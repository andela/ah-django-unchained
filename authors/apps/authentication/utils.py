import os
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Method to Send emails


def send_link(email, subject, template, url, *args):
    token = ''
    saved_args = locals()
    if saved_args['template'] == 'email_verify_account.html':
        token = saved_args['args'][0]
    from_email, to_email = settings.EMAIL_HOST_USER, [email]
    site_url = os.getenv('APP_BASE_URL')
    link_url = str(site_url) + \
        url + '{}/'.format(token)
    link_article = url
    message = render_to_string(
        template, {
            'user': to_email,
            'domain': link_url,
            'token': token,
            'username': to_email,
            'link': link_url,
            'link_article': link_article
        })

    send_mail(subject, '', from_email,
              [to_email, ], html_message=message, fail_silently=False)
