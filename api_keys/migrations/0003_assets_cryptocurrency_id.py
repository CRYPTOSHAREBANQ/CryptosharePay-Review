# Generated by Django 4.1.1 on 2022-09-25 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrency', '0001_initial'),
        ('api_keys', '0002_assets'),
    ]

    operations = [
        migrations.AddField(
            model_name='assets',
            name='cryptocurrency_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cryptocurrency.cryptocurrency'),
        ),
    ]
