from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.mail import send_mail
from notifications.signals import notify
from notifications.models import Notification
from authors.apps.friends.models import Friend
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from . import verbs


def follow_handler(sender, instance, created, **kwargs):
    """
    notfication handler for friends
    """
    # get the user that has been followed
    follower = instance.user_from
    followed = instance.user_to
    recipients = followed
    url = 'api/profiles/{}/follow/'.format(followed.username)
    notify.send(
        follower,
        recipient=recipients,
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
    # add the user's followers to the recipients list
    followers = Friend.objects.select_related(
        'user_from', 'user_to').filter(user_to=article_author.id).all()
    recipients = [get_user_model().objects.get(id=u.user_from_id) for u in list(followers)]

    url = "api/articles/"
    notify.send(
        article_author,
        recipient=recipients,
        description="{} posted an article on {}".format(
            article_author.username,
            instance.created.strftime('%d-%B-%Y %H:%M')),
        verb=verbs.ARTICLE_CREATION,
        action_object=instance,
        resource_url=url
        )


def favorited_article_comments_handler(sender, instance, created, **kwargs):
    """
    notification handler for favorited articles
    """
    recipients = []
    if instance.parent:
        parent_comment_author = instance.parent.author
        recipients.append(parent_comment_author)
    comment_author = instance.author
    article = instance.article
    description = "{} posted a comment to {} on {}"
    if article:
        # get all users that have favorited the article
        favorited_users = [fav.user for fav in Favorite.objects.filter(object_id=article.id).values('favorite')]
        recipients += favorited_users
        article_author = article.author
        if article_author.id != comment_author.id:
            recipients.append(article_author)
        resource_url = "{}/api/articles/".format(settings.DOMAIN)
        notify.send(
            comment_author,
            recipient=recipients,
            description=desc_string.format(
                comment_author.username,
                article or instance,
                instance.createdAt.strftime('%d-%B-%Y %H:%M')
                ),
            verb=verbs.COMMENT_CREATED,
            target=article or instance,
            action_object=instance,
            resource_url=resource_url
        )


def email_notification_handler(sender, instance, created, **kwargs):
    """
    notification handler for emails
    """
    recipient = instance.recipient
    description = instance.description
    token = recipient.token
    opt_out_link = '{}/api/notifications/unsubscribe/{}'.format(settings.DOMAIN, token)
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
