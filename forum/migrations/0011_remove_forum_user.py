# Generated by Django 5.1.1 on 2024-10-26 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_alter_forum_user_alter_forumkhusus_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='user',
        ),
    ]