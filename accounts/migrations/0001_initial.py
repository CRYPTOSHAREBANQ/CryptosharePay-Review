# Generated by Django 4.1.1 on 2022-09-24 03:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='country',
            fields=[
                ('country_id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=57)),
            ],
        ),
        migrations.CreateModel(
            name='business',
            fields=[
                ('business_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=57)),
                ('description', models.CharField(max_length=32)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
        migrations.CreateModel(
            name='api_key',
            fields=[
                ('api_key', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=15)),
                ('status', models.CharField(max_length=10)),
                ('business_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.business')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='country_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.country'),
        ),
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
