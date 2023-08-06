# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lily',
 'lily.assertion',
 'lily.assertion.management',
 'lily.assertion.management.commands',
 'lily.asynchronous',
 'lily.base',
 'lily.base.management',
 'lily.base.management.commands',
 'lily.cli',
 'lily.conf',
 'lily.docs',
 'lily.docs.management',
 'lily.docs.management.commands',
 'lily.docs.renderers',
 'lily.docs.renderers.angular',
 'lily.docs.renderers.markdown',
 'lily.entrypoint',
 'lily.entrypoint.management',
 'lily.entrypoint.management.commands',
 'lily.migrator',
 'lily.migrator.management',
 'lily.migrator.management.commands',
 'lily.search',
 'lily.search.detector',
 'lily.search.latex',
 'lily.search.migrations',
 'lily.search.stopwords']

package_data = \
{'': ['*'],
 'lily': ['notebook/*', 'notebook/.ipynb_checkpoints/*'],
 'lily.search': ['dicts/*'],
 'lily.search.detector': ['data/*']}

install_requires = \
['Django>=3.2.11,<4.1.0',
 'PyYAML>=6.0,<7.0',
 'django-bulk-update>=2.2.0,<3.0.0',
 'django-click>=2.3.0,<3.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'hunspell>=0.5.5,<0.6.0',
 'inflect>=5.3.0,<6.0.0',
 'itsdangerous>=2.0.1,<3.0.0',
 'jsonschema>=4.3.1,<5.0.0',
 'langid>=1.1.6,<2.0.0',
 'lily-assistant>=1.2.4,<2.0.0',
 'orjson>=3.6.5,<4.0.0',
 'psycopg2-binary>=2.9.2,<3.0.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.26.0,<3.0.0',
 'trans>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['lily = lily.cli.cli:cli']}

setup_kwargs = {
    'name': 'lily',
    'version': '2.4.1',
    'description': 'Lily MicroService Framework for Humans',
    'long_description': '\n# WARNING: this project is still undergoing some heavy changes and is still quite poorly documented so if you\'re interested in using it, well do that at your own risk.\n\n# Lily - microservices by humans for humans\n\nLily is built around:\n- DDD (Domain Driven Design) = Commands + Events\n- TDD+ (Test Driven Development / Documentation)\n\n## Foundations\n\nLily was inspired by various existing tools and methodologies. In order to understand the philosophy of `Lily` one must udnerstand two basic concepts:\n- `COMMAND` - is a thing one can perform\n- `EVENT` - is a consequence of executing `COMMAND` (one `COMMAND` can lead to many events).\n\nIn `lily` we define commands that are raising (python\'s `raise`) various events that are captured by the main events loop (do not confuse with node.js event loop).\n\n## Prerequisites\n\nIt is assumed that each `lily` project was setup together with the [`lily-assistant` tool](https://github.com/cosphere-org/lily-assistant) and that `lily_assistant init <src_dir_name>` command was executed therefore:\n\n- `.lily` folder exists in the root directory of the project\n- `.lily/config.json` was defined.\n\n\n## Creating HTTP commands\n\n`Lily` enable very simple and semantic creation of commands using various transport mechanism (HTTP, Websockets, Async) in a one unified way.\n\nEach HTTP command is build around the same skeleton:\n\n```python\nfrom lily import (\n    command,\n    Meta,\n    name,\n    Input,\n    Output,\n    serializers,\n    Access,\n    HTTPCommands,\n)\n\nclass SampleCommands(HTTPCommands):\n    @command(\n        name=<NAME>,\n\n        meta=Meta(\n            title=<META_TITLE>,\n            description=<META_DESCRIPTION>,\n            domain=<META_DOMAIN>),\n\n        access=Access(access_list=<ACCESS_LIST>),\n\n        input=Input(body_parser=<BODY_PARSER>),\n\n        output=Output(serializer=<SERIALIZER>),\n    )\n    def <HTTP_VERB>(self, request):\n\n        raise self.event.<EXPECTED_EVENT>({\'some\': \'thing\'})\n```\n\n\n\nThe simplest are HTTP commands that can be defined in the following way:\n\n```python\nfrom lily import (\n    command,\n    Meta,\n    name,\n    Input,\n    Output,\n    serializers,\n    Access,\n    HTTPCommands,\n)\n\nclass SampleCommands(HTTPCommands):\n    @command(\n        name=name.Read(CatalogueItem),\n\n        meta=Meta(\n            title=\'Bulk Read Catalogue Items\',\n            domain=CATALOGUE),\n\n        access=Access(access_list=[\'ADMIN\']),\n\n        input=Input(body_parser=CatalogueItemParser),\n\n        output=Output(serializer=serializers.EmptySerializer),\n    )\n    def get(self, request):\n\n        raise self.event.Read({\'some\': \'thing\'})\n```\n\n\n### Names\nFIXME: add it ...\n\n## Creating Authorizer class\n\nEach `command` created in Lily can be protected from viewers who should not be\nable to access it. Currently one can pass to the `@command` decorator\n`access_list`  which is passed to the `Authorizer` class.\n\n```python\nfrom lily.base.events import EventFactory\n\n\nclass BaseAuthorizer(EventFactory):\n    """Minimal Authorizer Class."""\n\n    def __init__(self, access_list):\n        self.access_list = access_list\n\n    def authorize(self, request):\n        try:\n            return {\n                \'user_id\': request.META[\'HTTP_X_CS_USER_ID\'],\n                \'account_type\': request.META[\'HTTP_X_CS_ACCOUNT_TYPE\'],\n            }\n\n        except KeyError:\n            raise self.AccessDenied(\'ACCESS_DENIED\', context=request)\n\n    def log(self, authorize_data):\n        return authorize_data\n\n```\n\nBut naturally it can take any form you wish. For example:\n- it could expect `Authorization` header and perform `Bearer` token decoding\n- it could leverage the existence of `access_list` allowing one to apply some\nsophisticated `authorization` policy.\n\nAn example of fairly classical (jwt token based `Authorizer` would be):\n\n\n```python\nfrom lily import BaseAuthorizer\nfrom .token import AuthToken\n\n\nclass Authorizer(BaseAuthorizer):\n\n    def __init__(self, access_list):\n        self.access_list = access_list\n\n    def authorize(self, request):\n\n        try:\n            type_, token = request.META[\'HTTP_AUTHORIZATION\'].split()\n\n        except KeyError:\n            raise self.AuthError(\'COULD_NOT_FIND_AUTH_TOKEN\')\n\n        else:\n            if type_.lower().strip() != \'bearer\':\n                raise self.AuthError(\'COULD_NOT_FIND_AUTH_TOKEN\')\n\n        account = AuthToken.decode(token)\n\n        if account.type not in self.access_list:\n            raise self.AccessDenied(\'ACCESS_DENIED\')\n\n        # -- return the enrichment that should be available as\n        # -- `request.access` attribute\n        return {\'account\': account}\n\n    def log(self, authorize_data):\n        return {\n            \'account_id\': authorize_data[\'account\'].id\n        }\n\n```\n\nNotice how above custom `Authorizer` class inherits from `BaseAuthorizer`.\nIn order to enable custom `Authorizer` class one must set in the `settings.py`:\n\n```python\nLILY_AUTHORIZER_CLASS = \'account.authorizer.Authorizer\'\n```\n\nwhere naturally the module path would depend on a specific project set up.\n\nFinally in order to use Authorization at the command level one must set in the @command definition:\n\n```python\nfrom lily import (\n    command,\n    Meta,\n    name,\n    Output,\n    serializers,\n    Access,\n    HTTPCommands,\n)\n\nclass SampleCommands(HTTPCommands):\n    @command(\n        name=name.Read(CatalogueItem),\n\n        meta=Meta(\n            title=\'Bulk Read Catalogue Items\',\n            domain=CATALOGUE),\n\n        access=Access(access_list=[\'ADMIN\']),\n\n        output=Output(serializer=serializers.EmptySerializer),\n    )\n    def get(self, request):\n\n        raise self.event.Read({\'some\': \'thing\'})\n```\n\nwhere `access` entry explicitly specifies who can access a particular command, that list will be injected to the `Authorizer` on each request to the server.\n\n## Rendering Commands (entrypoint)\n\nBy calling:\n\n```bash\nmake docs_render_markdown\n```\n\nOne will render `.lily/API.md` file which will contain the Markdown version of the commands specification.\n\n## Rendering API.md\n\nBy calling:\n\n```bash\nmake docs_render_commands\n```\n\nOne will render `.lily/commands/<version>.json` file which will contain the JSON version of the commands specification for a current version of the service. (this could be used for the automatic detection of Changelog).\n\n\n## Managing the state of database\n\nLily exposes three commands for managing migrations:\n\n```bash\nmake migrations_create\nmake migrations_bulk_read\nmake migrations_apply\n```\n\nWhich are just a wrappers around the commands exposed by django\'s built-in migration tool.\n\n## Full text search support\nFIXME: add it ...\n\n',
    'author': 'CoSphere Team',
    'author_email': 'contact@cosphere.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cosphere-org/lily',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.9,<3.10.0',
}


setup(**setup_kwargs)
