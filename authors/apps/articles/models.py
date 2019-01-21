from django.db import models
from authors.apps.authentication.models import User

from cloudinary.models import CloudinaryField


class Article(models.Model):
    """
    This is the Article model that is used to handle CRUD on articles
    """
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)
    description = models.CharField(max_length=50, blank=False)
    images = CloudinaryField(blank=True, default='No image', null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, blank=False, unique=True)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
