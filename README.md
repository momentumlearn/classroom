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

### .env

This application is configured via environment variables. In lieu of using environment variables, you can copy the file `config/.env.sample` to `config/.env` and then edit this file. Note that by default, debug mode is **off**, and that you need to set the environment variable `DEBUG` or use the `config/.env` file to turn debug mode on.

If you add new configuration that might change on environment, please use the environ package (see the top of `config/settings.py`) and environment variables to set up that configuration.

## Deployment

This application is currently deployed on AWS Elastic Beanstalk and all files under [.ebextensions](.ebextensions/) are related to that deployment.
