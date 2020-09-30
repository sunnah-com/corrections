# Overview

This is hadith corrections app.

python 3+ is required to run the project.

# Getting started

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
export FLASK_ENV=development FLASK_APP=main.py
flask run --host=0.0.0.0
```

Or alternatively use `docker-compose` inside `frontend` directory which will give a full environment with a MySQL instance loaded with a sample dataset:

```bash
docker-compose up
```

* Use `--build` option to re-build.
* Use the `-d` option to run in detached mode.

You can then visit [localhost:5500](http://localhost:5500) to verify that it's running on your machine.

## Deployment

Configuration files are located at `env.local` and `uwsgi.ini`.

A production ready uWSGI daemon (uwsgi socket exposed on port 5500) can be started with:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

The production backend is deployed at https://l7jwlmg0h3.execute-api.us-west-2.amazonaws.com/prod

## Request schema

The request to submit correction should be similar to:

```json
{
    "urn": "123",
    "attr": "body",
    "val": "modified body text here",
    "lang": "en",
    "comment": "fixed spelling",
    "queue": "global",
    "submittedBy": "someone@example.com",
}
```

## How to get api key

You will need an API key to access this data, which you may request by [creating an issue](https://github.com/sunnah-com/api/issues/new?template=request-for-api-access.md&title=Request+for+API+access%3A+%5BYour+Name%5D) on our GitHub repo.
