# Generated by Django 4.2.7 on 2023-12-09 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
