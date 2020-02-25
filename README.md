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

### Database

This application requires PostgreSQL as its database. For development, the default settings are a database with the name `classroom`, owned by a user with the name `classroom` and no password. To set this up locally, run:

```sh
createuser -d classroom
createdb -U classroom classroom
```
