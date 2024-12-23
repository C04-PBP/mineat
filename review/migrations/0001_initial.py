# Generated by Django 5.1.1 on 2024-10-22 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fnb', '0002_fnb_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('text', models.TextField()),
                ('fnb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_fnb', to='fnb.fnb')),
            ],
        ),
    ]
