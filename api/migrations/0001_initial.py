# Generated by Django 4.2.2 on 2023-06-22 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1255)),
                ('type', models.CharField(choices=[('B', 'BackEnd'), ('F', 'FrontEnd'), ('I', 'IOS'), ('A', 'Android')], max_length=1)),
                ('author_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
