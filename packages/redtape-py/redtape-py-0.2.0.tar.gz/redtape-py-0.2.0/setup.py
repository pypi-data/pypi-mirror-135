# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redtape', 'redtape.specification']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'attrs>=21.4.0,<22.0.0',
 'cattrs>=1.10.0,<2.0.0',
 'pre-commit>=2.16.0,<3.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'rich==11',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['redtape = redtape.cli:main']}

setup_kwargs = {
    'name': 'redtape-py',
    'version': '0.2.0',
    'description': 'A permission management tool for AWS Redshift.',
    'long_description': '# Redtape\n\n:ribbon: A permission management tool for AWS Redshift, with plans to extend it to other database systems. Inspired by [permifrost](https://gitlab.com/gitlab-data/permifrost/), and [pgbedrock](https://github.com/Squarespace/pgbedrock).\n\n## Installing\n\n### Repo\n\nClone this repo and install with `poetry`:\n\n```sh\ngit clone git@github.com:tomasfarias/redtape.git redtape\ncd redtape\npoetry install\n```\n\n### PyPI\n\nInstall with `pip`:\n\n```sh\npython -m pip install redtape\n```\n\n## Usage\n\n``` sh\n❯ redtape run --help\nUsage: redtape run [OPTIONS] [SPEC_FILE]\n\n  Run the queries necessary to apply a specification file.\n\nArguments:\n  [SPEC_FILE]  A specification or a path to a file containing it.\n\nOptions:\n  --dry / --no-dry                Print changes but do not run them.\n                                  [default: no-dry]\n  --skip-validate / --no-skip-validate\n                                  Skip specification file validation.\n                                  [default: no-skip-validate]\n  --user TEXT                     Apply operations only to users named as\n                                  provided.\n  --group TEXT                    Apply operations only to groups named as\n                                  provided.\n  --operation [CREATE|DROP|DROP_FROM_GROUP|GRANT|REVOKE|ADD_TO_GROUP]\n                                  Apply only provided operations.\n  --dbname TEXT                   A Redshift database name to connect to.\n  --host TEXT                     The host where a Redshift cluster is\n                                  located.\n  --port TEXT                     The port where a Redshift cluster is\n                                  located.\n  --database-user TEXT            A user to connect to Redshift. The user\n                                  should have user-management permissions.\n  --password TEXT                 The passaword of the given Redshift\n                                  username.\n  --connection-string TEXT        A connection string to connect to Redshift.\n  --quiet / --no-quiet            Show no output except of validation errors,\n                                  run errors, and queries.  [default: no-\n                                  quiet]\n  --help                          Show this message and exit.\n```\n\n## Specification file\n\nA YAML specification file is used to define groups, users, and their corresponding privileges.\n\nSample:\n\n``` yaml\ngroups:\n    - name: group_name\n        privileges:\n            table:\n                select:\n                    - table_name\n                    - ...\n                insert:\n                    - table_name\n                    - ...\n                update:\n                    - table_name\n                    - ...\n                drop:\n                    - table_name\n                    - ...\n                delete:\n                    - table_name\n                    - ...\n                references:\n                    - table_name\n                    - ...\n\n            database:\n                create:\n                    - database_name\n                    - ...\n                temporary:\n                    - database_name\n                    - ...\n                temp:\n                    - database_name\n                    - ...\n\n            schema:\n                create:\n                    - schema_name\n                    - ...\n                usage:\n                    - schema_name\n                    - ...\n\n            function:\n                execute:\n                    - function_name\n                    - ...\n\n            procedure:\n                execute:\n                    - function_name\n                    - ...\n\n            language:\n                usage:\n                    - language_name\n                    - ...\n\nusers:\n    - name: group_name\n        is_superuser: boolean\n        member_of:\n            - group_name\n            - ...\n        password:\n            type: str\n            value: str\n        privileges:\n            table:\n                select:\n                    - table_name\n                    - ...\n                insert:\n                    - table_name\n                    - ...\n                update:\n                    - table_name\n                    - ...\n                drop:\n                    - table_name\n                    - ...\n                delete:\n                    - table_name\n                    - ...\n                references:\n                    - table_name\n                    - ...\n\n            database:\n                create:\n                    - database_name\n                    - ...\n                temporary:\n                    - database_name\n                    - ...\n                temp:\n                    - database_name\n                    - ...\n\n            schema:\n                create:\n                    - schema_name\n                    - ...\n                usage:\n                    - schema_name\n                    - ...\n\n            function:\n                execute:\n                    - function_name\n                    - ...\n\n            procedure:\n                execute:\n                    - function_name\n                    - ...\n\n            language:\n                usage:\n                    - language_name\n                    - ...\n```\n\n# To do\n\n`redtape` should be considered in Alpha status: things may break, and test coverage is low. The following tasks are planned for a 1.0.0 release:\n* Increase and track test coverage.\n* Documentation.\n* Support for wildcard (`*`) in specifcation file.\n* Support for ownership.\n* Support for `ASSUMEROLE`.\n* Support for `EXTERNAL` objects.\n* Complete support for `mypy` static type-checking.\n\n# License\n\nMIT\n',
    'author': 'Tomás Farías Santana',
    'author_email': 'tomas@tomasfarias.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
