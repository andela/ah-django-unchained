from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from ..authentication.models import User, UserManager


class UserProfile(models.Model):
    """
    This class contains  models relating to user profile. 
    It has a one to one relationship with User model class.
    An intance of this class is created during user registration by calling 
    the create profile in the post_save function
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # A char field to hold bio data
    bio = models.TextField(max_length=200, default='')

    # A choice field to hold multiple choice
    gender_choices = (('M', 'MALE'), ('F', 'FEMALE'))
    gender = models.CharField(
        max_length=10, choices=gender_choices, default='M')

    # cloudinary field
    profile_image = CloudinaryField('image', null=True, default='', blank=True)

    # A char field for the First name
    first_name = models.CharField(max_length=100, default='')

    # A char field for the user Last name
    last_name = models.CharField(max_length=100, default='')

    # create a slug for the user name
    slug = models.SlugField(null=True, blank=True)

    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

# method to create a new profile


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        return user_profile


post_save.connect(create_profile, sender=User)

# method to set the slug


def create_slug_receiver(sender, instance, **kwargs):
    slug = slugify(instance.user.username)
    instance.slug = slug


pre_save.connect(create_slug_receiver, sender=UserProfile)
