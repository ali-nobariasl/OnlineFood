from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, message, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def detectUser(user):
    if user.role == 1:
        redirect = "vendordashboard"
        return redirect
    elif user.role == 2:
        redirect = "custdashboard"
        return redirect
    elif user.role == None and user.is_superuser:
        redirect = "/admin"
        return redirect


def send_verification_email(request, user, mail_subject, mail_template):

    # from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(
        mail_template,
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )

    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    # mail.content_subtype = "html"
    mail.send()


def send_notification(mail_subject, mail_template, context):
    # from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context["user"].email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
