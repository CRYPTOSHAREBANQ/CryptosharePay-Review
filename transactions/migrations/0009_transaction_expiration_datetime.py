# Generated by Django 4.1.1 on 2022-09-29 01:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_transaction_cryptocurrency_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 5, 1, 41, 18, 519597, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
