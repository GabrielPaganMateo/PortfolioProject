# Generated by Django 4.2.1 on 2023-06-09 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Resume_Collect', '0020_opening_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opening',
            name='user',
        ),
    ]
