# Generated by Django 4.1.13 on 2024-03-20 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Just_type_api', '0012_alter_user_errors_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_data',
            old_name='userId',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='user_experience',
            old_name='userId',
            new_name='user_id',
        ),
    ]
