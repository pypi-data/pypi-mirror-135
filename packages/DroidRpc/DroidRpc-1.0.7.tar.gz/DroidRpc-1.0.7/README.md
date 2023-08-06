# Droid v3
This repo is responsible for the definitions and deployments of the bots.
It contains:
  - Bot code
  - Bot test code
  - Dockerfiles to build bot images (each bot has its own)
  - K8s files that define the bot microservices
  - Skaffold files which define the microservice deployment pipeline (each microservice has its own)

## How to use this
- python 3.9.5 Required
- create .env file refer to ex.env variable
- setup your environment using venv or pipenv, and activate
- use pyenv is recomended for python environment version https://realpython.com/intro-to-pyenv/
- run `pip install -r installer/requirements.txt`, or if you plan on testing it, use `installer/test_requirements.txt`. If the installation throws an error like this: `ERROR: No matching distribution found for psycopg2==2.9.2`, edit `installer/basic_requirements.txt` on line 7 to `psycopg2-binary==2.9.2` and re-run that command. Don't forget to undo the change after `pip install` is done
- setup your environment variable, consult `ex.env` file as a guide. Copy that file, make modifications, and rename it to `.env`

## Notes on testing
- make sure you install the requirements from `installer/test_requirements.txt` file
- we are using `pytest` as the test framework, so you can put fixtures in the `conftest.py` file and your tests in `tests` folder.
- make sure to prefix the names of your test files (and test functions inside of them) with `test_`. For example:
  ```
  # file name: tests/test_user.py

  def test_user(user) -> None:
    assert user is not None
  ```
- run the tests with this command: `pytest -s`. This will run all tests in `tests` folder, the `-s` flag is used to show all `print()` functions that will otherwise be hidden. You can also run the test files individually like so: `pytest -s tests/test_user.py`
- consult [Pytest documentation](https://pytest.org/) or [pytest-django documentation](https://pytest-django.readthedocs.io/) for more information

## Notes on localisation
- install `gettext` from your OS's package manager (`sudo apt install gettext` in Ubuntu)
- import `gettext` on the file you want to have your translations in like so:
  ```
  from django.utils.translation import gettext as _
  ```
- mark the texts you want to be translated like this:

  ```
  print(_("key"))
  message: str = _("another key")
  ```
- run `./manage makemessages -a` **every time** you add new keys or edit existing ones to save the changes and register your keys.
- edit `locale/en_US/LC_MESSAGES/django.po` (or `locale/zh_Hant/LC_MESSAGES/django.po`) and add your translations in `msgstr` fields
- when finished, run `./manage.py compilemessages` to compile your changes, this will create `*.mo` files alongside the `.po` files
- consult [Django documentation](https://docs.djangoproject.com/en/3.2/topics/i18n/translation) for more information

## INSTALL CLIENTS
### using pip
```
pip install git+https://redloratech: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@github.com/asklora/DROID-V3.git@v-1.0.3-alpha#egg=DroidRpc
```
### or add in requirements.txt this line
```
DroidRpc @ git+https://github.com/asklora/DROID-V3.git@8a6726387dae98e3caf1bd7bd637ee7154044b02
```
# Contents
```
DROID-V3/
┣ DroidRpc/
┃ ┣ client/
┃ ┣ modules/
┃ ┣ proto/
┃ ┗ botrpc.py
┣ config/
┃ ┣ settings/
┃ ┣ __init__.py
┃ ┣ asgi.py
┃ ┣ urls.py
┃ ┣ var.py
┃ ┗ wsgi.py
┣ core/
┃ ┣ applications/
┃ ┣ bot/
┃ ┃ ┣ factory/
┃ ┃ ┣ migrations/
┃ ┃ ┣ modules/
┃ ┃ ┃ ┣ classic/
┃ ┃ ┃ ┣ ucdc/
┃ ┃ ┃ ┣ uno/
┃ ┃ ┃ ┗ __init__.py
┃ ┃ ┗ ...
┃ ┣ master/
┃ ┣ services/
┃ ┣ universe/
┃ ┗ utils/
┣ deployment/
┃ ┣ container/
┃ ┣ kubernetes/
┃ ┗ skaffold/
┣ installer/
┃ ┣ script/
┃ ┣ basic_requirements.txt
┃ ┣ requirements.txt
┃ ┗ test_requirements.txt
┣ locale/
┣ static/
┣ templates/
┣ tests/
┣ .env
┣ .gitignore
┣ README.md
┣ conftest.py
┣ ex.env
┣ main.py
┣ manage.py
┣ pytest.ini
┗ setup.py
```
## **DroidRpc/**
Contains code and .proto files for gRPC connections.

- **client/**  
  Contains a test client for gRPC connections.
- **modules/**  
  Contains the grpc-tools generated frameworks and messages.
- **proto**  
  Contains the .proto files for gRPC.

## **core/**
Contains the main source code of DROID-V3.
- **applications/**  
  ?????
- **[bot/](core/bot/README.md)**  
  Contains the main code for the bots.  
  - **factory/**  
  Contains the core functionality of the bots, and abstract classes/methods.
  - **migrations/**  
    ?????
  - **modules/**  
    Contains the bot modules (i.e. classic, uno, ucdc, etc.).  
    These extend core to create the bot images.
- **master/**  
  ?????
- **services/**  
  ?????
- **universe/**  
  ?????
- **utils/**  
  ?????

## **[deployment/](deployment/README.md)**
Contains the deployment code/yamls.
- **container/**  
  Contains the .Dockerfiles.
- **kubernetes/**  
  Contains the microservice deployments, services, configmaps, and secrets.
- **skaffold/**  
  Contains the Skaffold config files - these define the CI/CD pipeline.  
  Each microservice has its own config, and imports the core config as a module.

## **installer/**
Contains the requirements.txt and setup scripts.  
*NOTE: This should probably be removed as the scripts are coded into the core.Dockerfile already. Requirements can be moved into the core/bot/core/ directory.*
- **script/**  
  Contains the setup bash scripts

## **locale/**
contains translation package

## **static/**
Contains CSS used by django for front-end.

## **templates/**
Contains HTML used by django for front-end.

## **tests/**
Contains the tests for everything(?).
?????

## **conftest.py**
?????

## **ex.py**
?????

## **main.py**
?????

## **manage.py**
?????

## **pyteest.ini**
?????
