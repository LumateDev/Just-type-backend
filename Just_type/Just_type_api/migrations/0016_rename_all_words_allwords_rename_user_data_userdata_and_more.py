# Generated by Django 4.1.13 on 2024-03-27 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Just_type_api', '0015_alter_user_data_average_wpm_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='All_Words',
            new_name='AllWords',
        ),
        migrations.RenameModel(
            old_name='user_data',
            new_name='UserData',
        ),
        migrations.RenameModel(
            old_name='User_Errors',
            new_name='UserErrors',
        ),
        migrations.RenameModel(
            old_name='User_Experience',
            new_name='UserExperience',
        ),
    ]
