from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_account_activation_email(email, email_token):
    subject = "Your account needs to be verified"
    email_from = settings.DEFAULT_FROM_EMAIL

    activation_link = f'http://127.0.0.1:8000/accounts/activate/{email_token}'

    html_message = render_to_string(
        'emails/account_activation.html', {'activation_link': activation_link})
    plain_message = f'Hi, please verify your account by clicking the link: {activation_link}'

    send_mail(
        subject,
        plain_message,
        email_from,
        [email],
        html_message=html_message
    )
