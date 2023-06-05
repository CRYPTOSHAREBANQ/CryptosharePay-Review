# Generated by Django 4.1.1 on 2022-09-27 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digital_currency', '0001_initial'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='fiat_currency_amount',
            new_name='digital_currency_amount',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='fiat_currency_id',
        ),
        migrations.AddField(
            model_name='transaction',
            name='digital_currency_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='digital_currency.digital_currency'),
        ),
        migrations.DeleteModel(
            name='Fiat_Currency',
        ),
    ]
