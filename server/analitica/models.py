import hashlib
import random
import string

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import validate_ipv46_address, \
    validate_comma_separated_integer_list
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The email is required!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.tracking_id = user.make_tracking_id()
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be a member of the staff!')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have super powers!')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    # Used to get the admin user for whom tracking is being done.
    tracking_id = models.CharField(max_length=64, unique=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def make_tracking_id(self):
        tracking_id = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits)
                              for _ in range(16))
        tracking_id += self.email
        tracking_id = hashlib.sha256(tracking_id.encode('utf-8')).hexdigest()
        return tracking_id

    @property
    def serialize(self):
        """Returns serialized form of the User object."""
        return {
            'email': self.email,
            'tracking_id': self.tracking_id
        }


class Session(models.Model):
    # More session details such as browser engine, device and so on can be
    # included in this model. This will allow us to track what a user
    # (different than user model) did in their session.
    session_id = models.CharField(max_length=64, primary_key=True, null=False)
    browser = models.CharField(max_length=100, null=False)
    browser_version = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def serialize(self):
        """Returns serialized form of the User object."""
        return {
            'session_id': self.session_id,
            'browser': self.browser,
            'browser_version': self.browser_version
        }


class Visit(models.Model):
    # IP, Country and Screen Resolution might all change in a single session,
    # since user (different than user model) might switch to a VPN or change
    # their resolution, hence they are not included in the Session model.
    url = models.URLField(null=False)
    ip = models.CharField(validators=[validate_ipv46_address], max_length=100,
                          null=False)
    # As an optimization we can keep country and screen resolution data in a
    # separate table since they are bound to remain same for a large sub set
    # of entries. But as optimization is not needed at this point we can
    # leave it like this for now.
    country = models.CharField(max_length=100, null=False)
    screen_resolution = models.CharField(
        validators=[validate_comma_separated_integer_list], max_length=100,
        null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    @property
    def serialize(self):
        """Returns serialized form of the User object."""
        return {
            'url': self.url,
            'ip': self.ip,
            'country': self.country,
            'screen_resolution': self.screen_resolution,
            'created_at': self.created_at
        }
