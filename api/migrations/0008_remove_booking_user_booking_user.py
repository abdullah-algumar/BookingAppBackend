# Generated by Django 4.2.5 on 2024-03-24 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_booking_reservation_booking_end_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
