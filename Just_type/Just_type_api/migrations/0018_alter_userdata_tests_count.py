# Generated by Django 4.1.13 on 2024-03-27 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Just_type_api', '0017_alter_userexperience_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='tests_count',
            field=models.IntegerField(default=None),
        ),
    ]
