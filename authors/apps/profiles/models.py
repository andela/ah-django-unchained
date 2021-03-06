from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from ..authentication.models import User, UserManager


class UserProfile(models.Model):
    """
    This class contains  models relating to user profile. 
    It has a one to one relationship with User model class.
    An instance of this class is created during user registration by calling 
    the create profile in the post_save function
    """

    # create one to on relatioship with User model
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile"
                                )

    # A char field to hold bio data
    bio = models.TextField(max_length=200, blank=True)

    # A choice field to hold multiple choice
    gender_choices = (('M', 'MALE'), ('F', 'FEMALE'),
                      ('N', 'I PREFER NOT TO SAY'))
    gender = models.CharField(
        max_length=10, choices=gender_choices, default='N')

    # cloudinary field
    profile_image = models.URLField(blank=True,default='https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/user.png')

    # A char field for the First name
    first_name = models.CharField(max_length=100, blank=True)

    # A char field for the user Last name
    last_name = models.CharField(max_length=100, blank=True)

    # A char field for updated at
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()


def create_profile(sender, **kwargs):
    # method to create a new profile
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        return user_profile


post_save.connect(create_profile, sender=User)
