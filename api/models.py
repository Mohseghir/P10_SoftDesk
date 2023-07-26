from django.contrib.auth.models import User
from django.db import models


class Projects(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=512)
    TYPE_CHOICES = [
        ('B', 'BackEnd'),
        ('F', 'FrontEnd'),
        ('I', 'IOS'),
        ('A', 'Android'),
    ]
    project_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributors(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE,
                                related_name='contributors')
    ROLE_CHOICES = [
        ("A", "Author"),
        ("M", "Manager"),
        ("C", "Creator")
    ]
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)


class Issues(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    TAG_CHOICES = [
        ("B", "Bug"),
        ("I", "Improve"),
        ("T", "Task")
    ]
    tag = models.CharField(max_length=1, choices=TAG_CHOICES)
    PRIORITY_CHOICES = [
        ("H", "High"),
        ("M", "Medium"),
        ("L", "Low")
    ]
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(to=Projects, related_name="issues", on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("T", "To-Do"),
        ("I", "In-Progress"),
        ("C", "Closed")
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                      related_name='assigned_user')
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):

    description = models.CharField(max_length=2255)
    author_user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)


