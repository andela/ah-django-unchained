from django.db import models
from django.contrib.auth import get_user_model


class Friend(models.Model):
    """This is a model to build relationships between users"""

    # the user doing the following
    user_from = models.ForeignKey(
        get_user_model(),
        related_name='rel_from_set',
        on_delete=models.CASCADE)

    # the user being followed
    user_to = models.ForeignKey(
        get_user_model(),
        related_name='rel_to_set',
        on_delete=models.CASCADE)

    # time stamp associated with the action
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('user_from', 'user_to')

        def __str__(self):
            '{} follows {}'.format(
                self.user_from.username,
                self.user_to.username)

# adds following field to user dynamically
get_user_model().add_to_class('following', models.ManyToManyField(
    'self', through=Friend,
    related_name='followers',
    symmetrical=False
))
