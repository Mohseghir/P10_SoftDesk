from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

"""class User(AbstractUser):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=255)"""


class Project(models.Model):
    project_id = models.IntegerField(blank=False, null=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1255, blank=False)
    TYPE_CHOICES = (
        ('B', 'BackEnd'),
        ('F', 'FrontEnd'),
        ('I', 'IOS'),
        ('A', 'Android'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(to=User,
                                       on_delete=models.CASCADE)
