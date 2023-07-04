from django.conf import settings
from django.db import models


class Projects(models.Model):
    project_id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=8192)
    TYPE_CHOICES = (
        ('B', 'BackEnd'),
        ('F', 'FrontEnd'),
        ('I', 'IOS'),
        ('A', 'Android'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributors(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE,
                                   related_name='contributors')
    ROLE_CHOICES = (
        ("A", "Author"),
        ("M", "Manager"),
        ("C", "Creator")
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default="M")

    def __str__(self):
        return self.user_id


class Issues(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2255)
    issue_id = models.AutoField(primary_key=True)
    TAG_CHOICES = (
        ("B", "Bug"),
        ("I", "Improvement"),
        ("T", "Task")
    )
    tag = models.CharField(max_length=1, choices=TAG_CHOICES)
    PRIORITY_CHOICES = (
        ("H", "Hight"),
        ("M", "Medium"),
        ("L", "Low")
    )
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("T", "ToDo"),
        ("I", "InProgress"),
        ("C", "Closed")
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='authored_issues')
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2255)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, limit_choices_to={'is_staff': False})
    issue_id = models.ForeignKey(
        to=Issues, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment_id)
