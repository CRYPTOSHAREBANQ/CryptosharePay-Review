# Generated by Django 4.1.1 on 2022-10-05 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrency', '0003_alter_address_address_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Address_Subscription',
            new_name='AddressSubscription',
        ),
    ]
