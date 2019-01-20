import jwt
import os
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Method to Send emails
def send_link(self, email):
    payload = {'email':  email,
                "iat": datetime.now(),
                "exp": datetime.utcnow()
                + timedelta(minutes=5)}
    token = jwt.encode(payload,
                        settings.SECRET_KEY,
                        algorithm='HS256').decode()
    from_email, to_email = settings.EMAIL_HOST_USER, [email]
    subject = "Authors Haven Verification Link"
    site_url = os.getenv('EMAIL_VERIFICATION_URL')
    link_url = str(site_url) + \
        '/api/users/verify/{}/'.format(token)

    message = render_to_string(
        'email_verify_account.html', {
            'user': to_email,
            'domain': link_url,
            'token': token,
            'username': to_email,
            'link': link_url
        })

    send_mail(subject, '', from_email,
                [to_email, ], html_message=message, fail_silently=False)