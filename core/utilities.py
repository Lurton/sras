import datetime
import threading

import pytz
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader

from django.utils import timezone


def get_client_ip(request):
    """
    This is used for the authentication audits.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip_address = request.META.get("REMOTE_ADDR")

    if x_forwarded_for is not None:
        ip_address = x_forwarded_for.split(",")[0]

    return ip_address


def get_date_time_now(timezone_aware=True, formatting=None):
    """
    Returns a timezone aware timestamp as of now.
    """
    if timezone_aware:
        result = timezone.now()
    else:
        result = datetime.datetime.now().replace(tzinfo=pytz.utc)

    if formatting:
        response = result.strftime(formatting)
    else:
        response = result
    return response


class EmailThread(threading.Thread):
    """
    This class sends an email using threading via the AWS SES service.
    """
    def __init__(
        self,
        recipient,
        subject,
        template,
        email_data,
        cc=None,
        bcc=None,
        attachments=None,
        from_email=None,
        reply_to=None,
        headers=None
    ):
        threading.Thread.__init__(self)
        self.recipient = recipient
        self.subject = subject
        self.template = template
        self.email_data = email_data
        self.cc = cc
        self.bcc = bcc
        self.attachments = attachments
        self.from_email = from_email
        self.reply_to = reply_to
        self.headers = headers

        # Add the default key, value pairs to the `email_data`.
        self.email_data["site_title"] = settings.SITE_TITLE
        self.email_data["site_author"] = settings.SITE_AUTHOR
        self.email_data["site_description"] = settings.SITE_DESCRIPTION

    def run(self):
        html_template = loader.get_template(self.template)
        html_content = html_template.render(self.email_data)

        # Build the email message to be sent.
        message = EmailMessage(subject=self.subject, body=html_content)

        # Setup the email recipients etc.
        if self.recipient:
            if isinstance(self.recipient, list):
                message.to = self.recipient
            else:
                message.to = [self.recipient]

        if self.cc:
            if isinstance(self.cc, list):
                message.cc = self.cc
            else:
                message.cc = [self.cc]

        if self.bcc:
            if isinstance(self.bcc, list):
                message.bcc = self.bcc
            else:
                message.bcc = [self.bcc]

        if self.reply_to:
            if isinstance(self.reply_to, list):
                message.reply_to = self.reply_to
            else:
                message.reply_to = [self.reply_to]

        # Send additional email information to the service.
        if self.from_email:
            message.from_email = self.from_email

        if self.headers:
            message.extra_headers = self.headers

        # Add attachments if needed.
        if self.attachments:
            for attachment in self.attachments:
                message.attach(
                    filename=attachment["filename"],
                    content=attachment["content"],
                    mimetype=attachment["mimetype"]
                )

        # html message / email.
        message.content_subtype = "html"

        # Send the email.
        message.send()


def send_email(
    recipient,
    subject,
    template,
    email_data,
    cc=None,
    bcc=None,
    attachments=None,
    from_email=None,
    reply_to=None,
    headers=None
):
    """
    Sends normal e-mails.
    """
    if settings.EMAIL_ENABLED:
        # Start the email thread.
        try:
            EmailThread(
                recipient,
                subject,
                template,
                email_data,
                cc=cc,
                bcc=bcc,
                attachments=attachments,
                from_email=from_email,
                reply_to=reply_to,
                headers=headers
            ).start()
        except Exception:
            LOGGER.exception("send_email")