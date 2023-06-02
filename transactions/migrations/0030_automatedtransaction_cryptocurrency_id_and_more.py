# Generated by Django 4.1.2 on 2022-11-12 16:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrency', '0006_cryptocurrency_extra_data'),
        ('digital_currency', '0003_rename_digital_currency_name_digitalcurrency_name'),
        ('transactions', '0029_automatedtransaction_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='automatedtransaction',
            name='cryptocurrency_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cryptocurrency.cryptocurrency'),
        ),
        migrations.AddField(
            model_name='automatedtransaction',
            name='digital_currency_amount',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='automatedtransaction',
            name='digital_currency_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='digital_currency.digitalcurrency'),
        ),
        migrations.AddField(
            model_name='automatedtransaction',
            name='funds_source_address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='automatedtransaction',
            name='funds_source_address_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cryptocurrency.address'),
        ),
        migrations.AddField(
            model_name='automatedtransaction',
            name='funds_source_type',
            field=models.CharField(default='DEPOSIT_ADDRESS', max_length=30),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='expiration_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 13, 16, 56, 7, 132470, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
