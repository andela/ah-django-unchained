from django.conf import settings
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.urls import reverse
from notifications.signals import notify
from notifications.models import Notification
from authors.apps.friends.models import Friend
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from . import verbs


def follow_handler(sender, instance, created, **kwargs):
    """
    notification handler for friends
    """
    # get the user that has been followed
    follower = instance.user_from
    followed = instance.user_to
    recipient = followed
    if recipient.email_notification_subscription is False:
        return
    url = 'api/profiles/{}'.format(followed.username)
    notify.send(
        follower,
        recipient=recipient,
        description="{} followed you on {}".format(follower.username, instance.created_at.strftime('%d-%B-%Y %H:%M')),
        verb=verbs.USER_FOLLOWING,
        action_object=instance,
        target=followed,
        resource_url=url
        )


def article_handler(sender, instance, created, **kwargs):
    """
    notification handler for articles
    """
    article_author = instance.author
    followers = Friend.objects.select_related(
        'user_from').filter(user_to=article_author.id).all()
    # add the author's followers to the recipients list
    recipients = [User.objects.get(id=u.user_from_id) for u in followers]
    # add only the subscribed followers to the recipients list
    subsribed_users = [user for user in recipients if user.app_notification_subscription is True]
    if not subsribed_users:
        return
    for user in subsribed_users:
        url = reverse("articles:publish_article", kwargs={'slug': instance.slug})
        if instance.is_published:
            notify.send(
                article_author,
                recipient=user,
                description="{} posted an article on {}".format(
                    article_author.username,
                    instance.modified.strftime('%d-%B-%Y %H:%M')),
                verb=verbs.ARTICLE_CREATION,
                action_object=instance,
                resource_url=url
                )
        return False


def email_notification_handler(sender, instance, created, **kwargs):
    """
    notification handler for emails
    """
    user = instance.recipient
    recipient = User.objects.get(email=user)
    if recipient.email_notification_subscription is False:
        return
    description = instance.description
    token = recipient.token
    opt_out_link = '{}/api/notifications/unsubscribe/{}'.format(
        settings.DOMAIN, token
        )
    try:
        resource_url = instance.data['resource_url']
    except TypeError:
        resource_url = "api/articles/"
    html_content = render_to_string('email_notification.html', context={
        "opt_out_link": opt_out_link,
        "username": recipient.username,
        "description": description,
        "resource_url": resource_url
    })
    send_mail(
        "User Notification",
        '',
        'django_unchained@gmail.com',
        [recipient.email],
        html_message=html_content)


post_save.connect(follow_handler, sender=Friend, weak=False)
post_save.connect(article_handler, sender=Article, weak=False)
post_save.connect(email_notification_handler, sender=Notification)
