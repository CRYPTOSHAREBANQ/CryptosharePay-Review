# Generated by Django 4.1.1 on 2022-09-27 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_rename_fiat_currency_amount_transaction_digital_currency_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='state',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='transaction_ins',
            name='external_transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction_outs',
            name='external_transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction_book',
            name='registry_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
