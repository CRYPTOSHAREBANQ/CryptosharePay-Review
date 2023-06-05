# Generated by Django 4.1.1 on 2022-09-25 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_keys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=12)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=20)),
                ('api_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_keys.api_key')),
            ],
        ),
    ]
