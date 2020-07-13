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
pip install -r requirements.txt
export FLASK_ENV=development FLASK_APP=main.py
flask run --host=0.0.0.0
```

Or alternatively use `docker-compose` which will give a full environment with a MySQL instance loaded with a sample dataset:

```bash
docker-compose up
```

* Use `--build` option to re-build.
* Use the `-d` option to run in detached mode.

You can then visit [localhost:5000](http://localhost:5000) to verify that it's running on your machine. Or, alternatively:

```bash
$ curl http://localhost:5000
```

## Deployment

Configuration files are located at `env.local` and `uwsgi.ini`.

A production ready uWSGI daemon (uwsgi socket exposed on port 5001) can be started with:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## Request schema

The request to submit correction should be similar to:

```json
{
    "urn": "123",
    "attr": "matn",
    "val": "modified matn",
    "comment": "a damma was missing",
    "submittedBy": "hasan",
}
```
