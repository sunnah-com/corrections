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

- Use `--build` option to re-build.
- Use the `-d` option to run in detached mode.

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
  "submittedBy": "someone@example.com"
}
```

## How to get api key

You will need an API key to access this data, which you may request by [creating an issue](https://github.com/sunnah-com/api/issues/new?template=request-for-api-access.md&title=Request+for+API+access%3A+%5BYour+Name%5D) on our GitHub repo.

## How to setup flask mail server configs

For detailed documentation on what each config mean, please vist: https://pythonhosted.org/Flask-Mail/

For the following configs, I have taken gmail as an example.

1. The server is "smtp.gmail.com".
2. The port must match the type of security used.

   - If using STARTTLS with MAIL_USE_TLS = True, then use MAIL_PORT = 587.
   - If using SSL/TLS directly with MAIL_USE_SSL = True, then use MAIL_PORT = 465.
   - Enable either STARTTLS or SSL/TLS, not both.

3. Depending on your Google account's security settings, you may need to generate and use an [app password](https://security.google.com/settings/security/apppasswords) rather than the account password. This may also require enabling 2-step verification. You should probably set this up anyway.

Configurations

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = 'app password generated in step 3'
```

Example of email function execution

```
m = EMail()

ctx = {
	'email': 'someone@outlook.com',
	'message': 'This is the rejected reason',
	'attr': "'<p>Narrated ''Aisha:<p>(the mother of the faithful believers) Al-Harith bin Hisham asked Allah''s Apostle \"O Allah''s Apostle! How is the Divine Inspiration revealed to you?\" Allah''s Apostle replied, \"Sometimes it is (revealed) like the ringing of a bell, this form of Inspiration is the hardest of all and then this state passes off after I have grasped what is inspired. Sometimes the Angel comes in the form of a man and talks to me and I grasp whatever he says.\" ''Aisha added: Verily I saw the Prophet being inspired divinely on a very cold day and noticed the sweat dropping from his forehead (as the Inspiration was over).\r\n<p>'",
	'modifiedBy': 'Fahad Hayat',
	'modifiedText': 'Some text modified in the Hadith'
      }

m.send_mail(template='email/rejected.html', ctx=ctx, recipients=['someone@outlook.com'] )
```
