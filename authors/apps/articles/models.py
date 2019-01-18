import random

from django.db import models
from django.template.defaultfilters import slugify
from authors.apps.authentication.models import User

from cloudinary.models import CloudinaryField

class Article(models.Model):
    """
    This is the Article model that is used to handle CRUD on articles
    """
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False, unique=True)
    description = models.CharField(max_length=50, blank=False)
    images = CloudinaryField(blank=True, default='', null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, blank=False, unique=True)
    is_dispayed = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Generate a unique slug on save"""
        self.slug = slugify(self.title)
        new_slug = self.slug
        random_num = random.randint(1,10000)
        # Checks if a slug exists. If it does it appends a random number at the end
        while Article.objects.filter(slug=new_slug).exists():
            new_slug = '{}-{}'.format(self.slug, random_num)
            random_num += 1
        self.slug = new_slug
        super(Article, self).save(*args, **kwargs)
