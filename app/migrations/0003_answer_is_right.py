# Generated by Django 4.2.8 on 2023-12-30 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_right',
            field=models.BooleanField(default=False),
        ),
    ]
