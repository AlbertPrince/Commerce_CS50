# Generated by Django 4.1.2 on 2023-11-01 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_category_auctionlisting_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]