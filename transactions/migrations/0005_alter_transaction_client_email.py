# Generated by Django 4.1.1 on 2022-09-28 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_transaction_client_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='client_email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
