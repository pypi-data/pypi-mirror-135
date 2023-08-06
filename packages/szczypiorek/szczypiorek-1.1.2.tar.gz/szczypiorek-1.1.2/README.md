<img src="./assets/szczypiorek_logo.png" height="300">

# Szczypiorek - environment management for humans

**szczypiorek** allows one:
1. to define ones settings / credentials as a part of incredibly readable and flexible **yaml** format
2. using as an extra **template variables** and **imports**
3. and then define with minimal amount of code **environment parsers** which can be used to parse such yaml files
4. and allow one to use them directly in their python code
5. all of that on top of the mechanism allowing the secured storage and usage of most likely containing sensitive information yaml files.

## Getting Started

In order to start one needs to perform below steps.

### Creating yaml env file

It should contain some sort of settings, let's create one under `deploy/development.yml` folder:

```yaml
aws:
  secret: this is my secret
  is_sensitive: true
  age_days: 121
```

### Creating parser

Somewhere in your code create a parser (e.g. `env.py`):

```python
import szczypiorek as ev


class MyEnvParser(ev.EnvParser):

    aws_secret = ev.CharField()

    aws_is_sensitive = ev.BooleanField()

    aws_age_days = ev.IntegerField()


env = MyEnvParser().parse()

```

### Protect data stored in yamls

One must make sure that the yaml file will be protected therefore run in the terminal:
```bash
szczypiorek encrypt ./deploy
```

Make sure to add to `.gitignore`
```
.szczypiorek_encryption_key
deploy/development.yml
```

### Replace secrets on the fly

In certain situations, like when one created dynamical resources during the deployment phase, one would like to be able to replace certain parts of existing `.szczyp` file with some dynamical values.
In order to achieve that one would have to use the `replace` command:


```bash
szczypiorek replace -r a.b:12 -r a.g.f.secret:password
```

By default it would use the default encryption key and default szczyp file but one can overwrite it by passing extra arguments. Please run:

```bash
szczypiorek replace --help
```

To learn more.

## FAQ

### How and in which order szczypiorek resolves encryption key and environment gpg?

1. Encryption key is searched in various places in this order:
- `SZCZYPIOREK_ENCRYPTION_KEY` environment variable where it's expected that the **content** of the **encryption key** will be stored.
- `SZCZYPIOREK_ENCRYPTION_KEY_FILE` environment variable where the **path** to chosen **encryption key** file is stored
- if above is not found szczypiorek tries default `.szczypiorek_encryption_key` file.

2. Environment gpg is searched in various places in this order:
- `SZCZYPIOREK_ENVIRONMENT_GPG` environment variable where it's expected that the **content** of the **environment gpg** will be stored.
- `SZCZYPIOREK_ENVIRONMENT_GPG_FILE` environment variable where the **path** to chosen **environment gpg** file is stored
- if above is not found szczypiorek tries default `env.gpg` file.

### How szczypiorek behaves when deployed?

When deployed for the parser to work correctly one needs two things:
1. A single `env.gpg` file available in the root of the project
2. A `.szczypiorek_encryption_key` storing the secret generated during the `encrypt` phase. WARNING! Make sure that this file is not kept in the repository itself but rather created dynamically during the deployment phase. Till that time it could be stored in for example `github secrets` or similar system such as `AWS secrets`, `Azure Key Vault` etc.

### How szczypiorek behaves locally?

For the `szczypiorek` to work locally one needs 3 things:
1. One `gpg` file for example `development.gpg`
2. A environment variable `SZCZYPIOREK_ENVIRONMENT_GPG_FILE=development.gpg` pointing to that file's location
3. A `.szczypiorek_encryption_key` file where a secret for decryption is stored.

### One contributor changed gpg files would after PUSH & PULL sequence see the changes?

TODO: add it

### One contributor is changing the yaml files but the other cannot see those reflected in the gpg file?

TODO: add it

## The CLI - Available commands

FIXME: add it!!!
```bash
szczypiorek print-env cosphere_api.conf.env.api_env
```

## The Environment Parser - Available fields

TODO: add it

USE BELOW LEGACY AS INSPIRATION:

Use the below example as a inspiration regarding type of fields one can define.

```python

import szczypiorek as env


class MyEnvParser(env.EnvParser):

    secret_key = env.CharField()

    is_important = env.BooleanField()

    aws_url = env.URLField()

    number_of_workers = env.IntegerField()

    unit_price = env.FloatField()

```

Each field supports the following arguments:

- `required` (boolean) - if environment variable is required to be present
- `default` (target type) - default to be used in case environment variable was not found
- `allow_null` (boolean) - if environment variable can be nullable
- `description` (str) - where one can describe the purpose of a given field when the name itself is not enough to capture it.

Besides those some fields are supporting extra fields:

- `CharField`:

    - `min_length` - validates if minimum amount of characters was provided
    - `max_length` - validates if maximum amount of characters was provided


## The Environment YAML files - Reference

TODO: add it
    - decribe the usage of template variables

## TODOS

There's still a lot of work to do, even though the basic functionality of **szczypiorek** is production ready:

- [ ] **[HIGH PRIO]** enable versioning of secrets and a command which is able to clean up all unused secrets

- [ ] **[HIGH PRIO]** use https://github.com/squidfunk/mkdocs-material for docs

- [ ] **[HIGH PRIO]** host the docs on github pages https://www.mkdocs.org/user-guide/deploying-your-docs/

- [ ] **[HIGH PRIO]** replace the parsing mechanism with Pydantic models to make it more modern and more like python static typing.

- [ ] **[HIGH PRIO]** add an option to sync the secret of the admin

- [ ] **[LOW PRIO]** Enable imports in the yml files. It should take the following form:
```yaml
imports:
  - shared.yml
  - development.yml
```
And then when running `encrypt` one stores at the level of gpg files all its dependencies therefore making it self contained. Before creating the gpg file it could create structure like:
```yaml
- filename: shared.yml
  content: ...

- filename: development.yml
  content: ...

# MAIN FILE
- filename: integration.yml
  content: ...
```
When running `decrypt` it "unpacks" all files with warnings that existing ones would be overwritten. There will be an option to force it without messages. When `decrypting` in the parser the imports are taken into account and therefore applied right away so the resulting `env` is just a result of applying all dependencies.

- [ ] **[LOW PRIO]** support **DB_POSTGRES_CONNECT validator**:
* it expects certain fields to be present
* it allows fields mapping

- [ ] **[LOW PRIO]** support **SENTRY_PING validator**:
* it uses https://develop.sentry.dev/sdk/store/
* it just pings the API

- [ ] **[LOW PRIO]** support **OAUTH2_PING validator**:
* it just creates a OAUTH2 session and tries not to fail while doing this

- [ ] **[LOW PRIO]** support **API_PING validator**:
* it just pings the API
* it allows fields mapping

- [ ] **[LOW PRIO]** support **AWS_S3_CLOUDFRONT_PING validator**:
* it just pings the endpoint

- [ ] **[LOW PRIO]** support **AWS_S3_BUCKET_LIST validator**:
* it just lists the bucket

- [ ] **[LOW PRIO]** support **AWS_POLLY_RENDER_SAMPLE validator**:
* it renders simple text

- [ ] **[LOW PRIO]** handle ROTATION of the **szczypiorek** secret itself. One can with one command run:
* `decrypt`
* render new key
* `encrypt`

- [ ] **[LOW PRIO]** support PRODUCTION gpg file where all validators etc are removed only the essential parts are left
