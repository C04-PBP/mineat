# Generated by Django 5.1.2 on 2024-10-26 03:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_alter_forum_user_alter_forumkhusus_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_umum', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='forumkhusus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_khusus', to=settings.AUTH_USER_MODEL),
        ),
    ]
