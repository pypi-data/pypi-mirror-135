# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spkrepo', 'spkrepo.tests', 'spkrepo.views']

package_data = \
{'': ['*'],
 'spkrepo': ['static/css/*',
             'static/fonts/*',
             'static/js/*',
             'templates/*',
             'templates/frontend/*',
             'templates/security/*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'bcrypt>=3.1.7,<4.0.0',
 'click>=8.0.0,<9.0.0',
 'configparser>=5.0.0,<6.0.0',
 'email_validator>=1.1.1,<2.0.0',
 'flask-admin>=1.5.6,<2.0.0',
 'flask-babelex>=0.9.4,<0.10.0',
 'flask-caching>=1.8.0,<2.0.0',
 'flask-debugtoolbar>=0.11.0,<0.12.0',
 'flask-login>=0.5.0,<0.6.0',
 'flask-mail>=0.9.1,<0.10.0',
 'flask-migrate>=3.0.0,<4.0.0',
 'flask-principal>=0.4.0,<0.5.0',
 'flask-restful>=0.3.8,<0.4.0',
 'flask-script>=2.0.6,<3.0.0',
 'flask-security>=3.0.0,<4.0.0',
 'flask-sqlalchemy>=2.4.1,<3.0.0',
 'flask-wtf>=1.0.0,<2.0.0',
 'flask>=2.0.0,<3.0.0',
 'ipaddress>=1.0.23,<2.0.0',
 'passlib>=1.7.2,<2.0.0',
 'pillow',
 'python-gnupg>=0.4.6,<0.5.0',
 'redis>=4.1.0,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'sqlalchemy>=1.3.17,<2.0.0',
 'text-unidecode>=1.3,<2.0',
 'wtforms>=2.3.3,<3.0.0']

setup_kwargs = {
    'name': 'spkrepo',
    'version': '0.2.1',
    'description': 'Synology Package Repository',
    'long_description': '# spkrepo\nSynology Package Repository\n\n![Build](https://img.shields.io/github/workflow/status/SynoCommunity/spkrepo/Build?style=for-the-badge)\n[![Discord](https://img.shields.io/discord/732558169863225384?color=7289DA&label=Discord&logo=Discord&logoColor=white&style=for-the-badge)](https://discord.gg/nnN9fgE7EF)\n\n\n## Development\n### Installation\n1. Install dependencies with `poetry install`\n2. Run the next commands in the virtual environment `poetry shell`\n3. Create the tables with `python manage.py db create`\n4. Populate the database with some fake packages with `python manage.py db populate`\n5. Add an user with `python manage.py user create -u Admin -e admin@admin.adm -p adminadmin`\n6. Grant the created user with Administrator permissions `python manage.py user add_role -u admin@admin.adm -r admin`\n7. Grant the created user with Package Administrator permissions `python manage.py user add_role -u admin@admin.adm -r package_admin`\n8. Grant the created user with Developer permissions `python manage.py user add_role -u admin@admin.adm -r developer`\n\nTo reset the environment, clean up with `python manage.py clean`.\n\n### Run\n1. Start the development server with `python manage.py runserver`\n2. Website is available at http://localhost:5000\n3. Admin interface is available at http://localhost:5000/admin\n4. NAS interface is available at http://localhost:5000/nas\n5. API is available at http://localhost:5000/api\n6. Run the test suite with `poetry run pytest -v`\n\n## Docker Compose Run\nIt is also possible to start a development environment with postgres database\nusing docker compose:\n1. Build and run `docker-compose up --build`\n2. On first run you can apply database migrations with `docker exec spkrepo_spkrepo_1 python manage.py db upgrade`.\n   Also run any other command that you need (populate the databse, create user) as mentioned above but by prefixing\n   with `docker exec {container_id} [...]`.\n3. Browse to http://localhost:5000\n4. To tear down the environment, run `docker-compose down --remove`\n\n## Deployment\n\n### Configuration\nCreate a config file `./config.py` to disable debug logs, connect to a database, set a secure key and optionally set a cache:\n\nUse `LC_CTYPE=C tr -cd \'[:print:]\' < /dev/urandom | head -c 64` or `base64 < /dev/urandom | head -c 64` to get a random string\n\n```python\nDEBUG = False\nTESTING = False\nSECRET_KEY = "Please-change-me-to-some-random-string"\nSQLALCHEMY_ECHO = False\nSQLALCHEMY_DATABASE_URI = "postgresql://user:pass@localhost/dbname"\n# https://pythonhosted.org/Flask-Caching/#configuring-flask-caching\nCACHE_TYPE= "simple"\n# For signing packages\nGNUPG_PATH= "/usr/local/bin/gpg"\n```\n\n\n### Docker\nExample usage:\n\n```bash\ndocker run -it --rm --name spkrepo -v $(pwd)/data:/data -p 8000:8000 ghcr.io/synocommunity/spkrepo\n```\n\nAdditional configuration can be mounted in the container and loaded by putting\nthe path into `SPKREPO_CONFIG` environment variable.\n\ne.g.\n```bash\ndocker run -it --rm --name spkrepo -v $(pwd)/data:/data -v $(pwd)/docker-config.py:/docker-config.py -e SPKREPO_CONFIG=/docker-config.py -p 8000:8000 ghcr.io/synocommunity/spkrepo\n```\n\n\n### Serve app via [a WSGI server](https://flask.palletsprojects.com/en/1.1.x/deploying/).\nExample:\n\n```bash\npip install gunicorn\nSPKREPO_CONFIG="$PWD/config.py" gunicorn -w 4 \'wsgi:app\'\n```\n',
    'author': 'Antoine Bertin',
    'author_email': 'diaoulael@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://synocommunity.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
