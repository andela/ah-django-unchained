from django.db import models
from ..articles.models import Article
from ..authentication.models import User


class Bookmarks(models.Model):
    """
    class for containg bookmarks model
    """
    article = models.OneToOneField(Article, on_delete='CASCADE')
    user = models.ForeignKey(User, on_delete='CASCADE')
    created_at = models.DateTimeField(auto_now_add=True)