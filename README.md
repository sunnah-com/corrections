# Sunnah.com Corrections App

## Overview

This is hadith corrections app.

python 3+ is required to run the project.

## Getting started

Please follow the instructions below.

First create a local `.env.local` configuration file and update values as needed.
A sample file is provided at `.env.local.sample`.

Run manually:

```bash
git clone REPO
cd REPO
python3 -m venv venv
source venv/bin/activate
pip install -r frontend/requirements.txt
cd frontend
export FLASK_ENV=development FLASK_APP=app
flask run --host=0.0.0.0
```

Or alternatively use `docker-compose` inside `frontend` directory which will give a full environment with a MySQL instance loaded with a sample dataset:

```bash
docker-compose up
```

- Use `--build` option to re-build.
- Use the `-d` option to run in detached mode.

You can then visit [localhost:5500](http://localhost:5500) to verify that it's running on your machine.

## Deployment

Configuration files are located at `env.local` and `uwsgi.ini`.

A production ready uWSGI daemon (uwsgi socket exposed on port 5500) can be started with:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

The corrections ingestor receives corrections (with an API key) at https://corrections.sunnah.com/submit.

## Request schema

The request to submit correction should be similar to:

```json
{
  "id": "a6407823-286c-455d-9874-8de0093336b2",
  "urn": "123",
  "attr": "body",
  "val": "modified body text here",
  "lang": "en",
  "comment": "fixed spelling",
  "queue": "global",
  "submittedBy": "someone@example.com"
}
```
_**Note**: `id` field is optional. It is autogenerated when not provided._

## How to get api key

You will need an API key to access this data, which you may request by [creating an issue](https://github.com/sunnah-com/api/issues/new?template=request-for-api-access.md&title=Request+for+API+access%3A+%5BYour+Name%5D) on our GitHub repo.

## How to setup flask mail server configs

For detailed documentation on what each config mean, please vist: https://pythonhosted.org/Flask-Mail/

For the following configs, I have taken gmail as an example.

1. The server is "smtp.gmail.com".
2. The port must match the type of security used.

   - If using `STARTTLS` with `MAIL_USE_TLS = True`, then use `MAIL_PORT = 587`.
   - If using `SSL/TLS` directly with `MAIL_USE_SSL = True`, then use `MAIL_PORT = 465`.
   - Enable either `STARTTLS` or `SSL/TLS`, not both.

3. Depending on your Google account's security settings, you may need to generate and use an [app password](https://security.google.com/settings/security/apppasswords) rather than the account password. This may also require enabling 2-step verification. You should probably set this up anyway.

Configurations

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = 'app password generated in step 3'
```

## How to Run Unit Tests
 
```bash
docker-compose --file docker-compose.test.yml run corrections
```

## Guidelines for Sending a Pull Request

1. Only change one thing at a time.
2. Don't mix a lot of formatting changes with logic change in the same pull request.
3. Keep code refactor and logic change in separate pull requests.
4. Squash your commits. When you address feedback, squash it as well. No one benefits from "addressed feedback" commit in the history.
5. Break down bigger changes into smaller separate pull requests.
6. If changing UI, attach a screenshot of how the changes look.
7. Reference the issue being fixed by adding the issue tag in the commit message.
8. Do not send a big change before first proposing it and getting a buy-in from the maintainer.
