from flask import render_template, current_app
from extensions import mail
import os


class EMail:
    """
    The class is responsible for sending mails to the individuals who have submitted a Hadith correction built on top of Flask-Mail
    """

    def __init__(self):
        self.m = mail

    def send(self, template=None, ctx=None, *args, **kwargs):
        """
        Send a templated e-mail using a similar signature as Flask-Mail:
        http://pythonhosted.org/Flask-Mail/

        Except, it also supports template rendering. If you want to use a template
        then just omit the body and html kwargs to Flask-Mail and instead supply
        a path to a template. It will auto-lookup and render text/html messages.

        Example:
            ctx = {'username': current_user, 'message': 'message in the body'}
            send(subject='Correction', recipients=[users_email],
                                template='layout/mail', ctx=ctx)

        :param subject:
        :param recipients:
        :param body:
        :param html:
        :param sender:
        :param cc:
        :param bcc:
        :param attachments:
        :param reply_to:
        :param date:
        :param charset:
        :param extra_headers:
        :param mail_options:
        :param rcpt_options:
        :param template:  Path to a template without the extension (File must be in the templates folder)
        :param ctx: Dictionary of anything you want in the template context
        :return: None
        """

        if template is not None:
            if "body" in kwargs:
                raise Exception("You cannot have both a template and body arg.")
            elif "html" in kwargs:
                raise Exception("You cannot have both a template and html arg.")

            kwargs["html"] = render_template(template, **ctx)

        self.m.send_message(
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            reply_to=current_app.config["MAIL_DEFAULT_SENDER"],
            *args,
            **kwargs
        )

        return None
