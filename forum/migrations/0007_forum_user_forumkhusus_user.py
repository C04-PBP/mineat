# Generated by Django 5.1.2 on 2024-10-25 11:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_remove_forum_user_forum_time_created_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forum_umum', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumkhusus',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forum_khusus', to=settings.AUTH_USER_MODEL),
        ),
    ]