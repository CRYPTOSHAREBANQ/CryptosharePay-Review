# Generated by Django 4.1.1 on 2022-09-27 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Digital_Currency',
            fields=[
                ('digital_currency_id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('digital_currency_name', models.CharField(max_length=50)),
                ('exchange_rate', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
