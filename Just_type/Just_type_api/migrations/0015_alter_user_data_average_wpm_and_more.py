# Generated by Django 4.1.13 on 2024-03-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Just_type_api', '0014_rename_averagewpm_user_data_average_wpm_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data',
            name='average_WPM',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='average_accuracy',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='best_WPM',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='best_accuracy',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='tests_count',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='user_experience',
            name='experience',
            field=models.FloatField(default=None),
        ),
    ]
