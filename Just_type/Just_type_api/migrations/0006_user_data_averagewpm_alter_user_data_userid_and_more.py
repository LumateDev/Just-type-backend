# Generated by Django 4.1.13 on 2024-03-19 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Just_type_api', '0005_remove_user_data_id_alter_user_data_userid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='averageWPM',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='userId',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_errors',
            name='userId',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
