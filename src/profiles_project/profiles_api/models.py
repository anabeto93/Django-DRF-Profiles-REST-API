from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):
    """ helps Django work with the custom user model. """

    def create_user(self, email, name, password=None):
        """ creates a new user profile """

        if not email:
            raise ValueError('Users must have an email address.')
        if not name:
            raise ValueError('Users must have a name.')


        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        #set the user's password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """ Creates adn saves a new superuser or admin. """

        if not password:
            raise ValueError('Password is required.')

        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """
    Reperesent a User profile in this system
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Get the User's full name"""
        return self.name

    def get_short_name(self):
        """ Used to get User's short name"""
        return self.name

    def __str__(self):
        """ Convert the object into a string"""

        return self.email
