# Generated by Django 4.1.13 on 2024-03-20 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Just_type_api', '0010_alter_user_errors_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_errors',
            name='user_id',
            field=models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_id', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user_id'),
        ),
    ]