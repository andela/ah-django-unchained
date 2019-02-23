from django.db import models
from authors.apps.authentication.models import User
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField
from simple_history.models import HistoricalRecords


class Article(models.Model):
    """
    This is the Article model that is used to handle CRUD on articles
    """
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    description = models.CharField(max_length=50, blank=True)
    images = CloudinaryField(blank=True, default='No image', null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, blank=False, unique=True)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    favorite = models.ManyToManyField(User, related_name='favorite',
                                      default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tagList = TaggableManager()
    user_id_likes = models.ManyToManyField(
        User, related_name='likes', blank=True)
    user_id_dislikes = models.ManyToManyField(
        User, related_name='dislikes', blank=True)

    class Meta:
        ordering = ['-created']


class ArticleRating(models.Model):
    """
    This is a model to handle article ratings
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.rate


class Comment(models.Model):
    """This is the Article model that is used to handle CRUD on articles"""

    parent = models.ForeignKey('self', null=True, blank=False,
                               on_delete=models.CASCADE,
                               related_name='threads')
    author = models.ForeignKey(User, related_name='author',
                               on_delete=models.CASCADE)

    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True,
                                related_name='comments')
    body = models.TextField(blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    user_id_likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    user_id_dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.body)

    class Meta:
        ordering = ['-createdAt']


class HighlightTextModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    article = models.ForeignKey(Article, related_name='highlight',
                                on_delete=models.CASCADE, null=True)
    selected_text = models.TextField(blank=True)
    start_highlight_position = models.IntegerField(blank=True, null=True)
    end_highlight_position = models.IntegerField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)

    class Meta:
        ordering = ['-createdAt']
