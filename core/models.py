from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class User(AbstractBaseUser):
    userId = ShortUUIDField(max_length=20, primary_key=True, unique=True, editable=False)
    firstName = models.CharField(max_length=25, blank=False, null=False)
    lastName = models.CharField(max_length=25, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=25, blank=False, null=False)
    phone = models.CharField(max_length=15)
    #organisations = models.ManyToManyField(Organisation)

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

