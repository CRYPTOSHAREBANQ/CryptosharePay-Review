# Generated by Django 4.1.1 on 2022-09-25 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrency',
            name='coingecko_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
