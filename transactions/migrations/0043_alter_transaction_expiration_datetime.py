# Generated by Django 3.2.16 on 2023-06-02 05:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0042_alter_transaction_expiration_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 3, 5, 50, 44, 328833, tzinfo=utc), null=True),
        ),
    ]
