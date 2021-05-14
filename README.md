# Momentum Classroom

This Django application is used to conduct self-evaluations for Momentum Learning.

## Set up for development

This application uses [Pipenv](https://pipenv.kennethreitz.org/en/latest/) to manage dependencies. To install all dependencies, run:

```sh
pipenv install
```

Pipenv requires several environment variables to be set. These are all set by running:

```sh
pipenv shell
```

You must do this before starting this application.

For deployment purposes, we also need a `requirements.txt` file. After installing any new packages via Pipenv, please run `make requirements.txt`.

### Database

This application requires PostgreSQL as its database. For development, the default settings are a database with the name `classroom`, owned by a user with the name `classroom` and no password. To set this up locally, run:

```sh
createuser -d classroom
createdb -U classroom classroom
```

#### Seeding skills data

Skills are listed in versioned markdown files and can be seeded to the database with the custom management command `load_skills` followed by the path to the file.

The naming convention is important as the script will assign versions to the skills based on the filename; the file should start with a lowercase `v` followed by a version number. For instance, a file named `v2-skills.md` will have skills saved with a version number 2.

Versioning the skills lets us keep backwards compatible data as we update skill sets on which we want to evaluate students.

```py
python ./manage.py load_skills skills.md
```

### .env

This application is configured via environment variables. In lieu of using environment variables, you can copy the file `config/.env.sample` to `config/.env` and then edit this file. Note that by default, debug mode is **off**, and that you need to set the environment variable `DEBUG` or use the `config/.env` file to turn debug mode on.

If you add new configuration that might change on environment, please use the environ package (see the top of `config/settings.py`) and environment variables to set up that configuration.

## Deployment

This application is currently deployed on AWS Elastic Beanstalk and all files under [.ebextensions](.ebextensions/) are related to that deployment.
