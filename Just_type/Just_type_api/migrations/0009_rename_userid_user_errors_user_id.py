# Generated by Django 4.1.13 on 2024-03-20 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Just_type_api', '0008_user_experience_remove_user_data_experience_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_errors',
            old_name='userId',
            new_name='user_id',
        ),
    ]
