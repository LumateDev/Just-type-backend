# Generated by Django 4.2.7 on 2023-11-25 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Just_type_api', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
