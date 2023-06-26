# Generated by Django 4.2.2 on 2023-06-23 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('A', 'Author'), ('M', 'Manager'), ('C', 'Creator')], default='M', max_length=1)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributors', to='api.project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
