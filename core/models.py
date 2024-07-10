from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from shortuuidfield import ShortUUIDField
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser):
    userId = ShortUUIDField(max_length=20, primary_key=True, unique=True, editable=False)
    firstName = models.CharField(max_length=25, blank=False, null=False, unique=True)
    lastName = models.CharField(max_length=25, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=25, blank=False, null=False)
    phone = models.CharField(max_length=15, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firsName','lastName', 'password', 'phone']

    def __str__(self):
        return self.userId


class Organisation(models.Model):
    orgId = ShortUUIDField(max_length=20, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=75, blank=False, null=False)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
