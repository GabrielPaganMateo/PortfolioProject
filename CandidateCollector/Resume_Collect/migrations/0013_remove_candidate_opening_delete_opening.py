# Generated by Django 4.2.1 on 2023-05-29 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Resume_Collect', '0012_alter_candidate_phone_alter_candidate_text_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='opening',
        ),
        migrations.DeleteModel(
            name='Opening',
        ),
    ]
