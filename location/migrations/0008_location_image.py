# Generated by Django 5.1.2 on 2024-10-25 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0007_location_trivia_alter_location_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='image',
            field=models.CharField(default='', max_length=511),
            preserve_default=False,
        ),
    ]