from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from shortuuidfield import ShortUUIDField
# Create your models here.

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)  # Assuming email is unique



class User(AbstractBaseUser):
    userId = ShortUUIDField(max_length=20, primary_key=True, unique=True, editable=False)
    firstName = models.CharField(max_length=25, blank=False, null=False, unique=True)
    lastName = models.CharField(max_length=25, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=25, blank=False, null=False)
    phone = models.CharField(max_length=15,blank=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firsName','lastName', 'password', 'phone']

    def __str__(self):
        return self.userId


class Organisation(models.Model):
    orgId = ShortUUIDField(max_length=20, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=75, blank=False, null=False)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
    
