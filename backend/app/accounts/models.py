from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    payment_plan = models.CharField(max_length=200, default='free')

