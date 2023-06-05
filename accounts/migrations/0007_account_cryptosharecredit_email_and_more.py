# Generated by Django 4.1.2 on 2022-11-12 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_account_security_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='cryptosharecredit_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='cryptosharecredit_linked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='cryptosharecredit_username',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
