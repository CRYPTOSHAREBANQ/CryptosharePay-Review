# Generated by Django 4.1.1 on 2022-09-24 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_api_key_business_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='api_key',
        ),
        migrations.DeleteModel(
            name='business',
        ),
    ]
