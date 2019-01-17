from django.db import models
from authors.apps.authentication.models import User
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField

class Article(models.Model):
    title = models.CharField(max_length=50, blank=False, unique=True)
    body = models.TextField(blank=False, unique=True)
    description = models.CharField(max_length=50, blank=False)
    images = CloudinaryField(blank=False, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs) 
