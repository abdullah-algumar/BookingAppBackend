# Generated by Django 4.2.5 on 2024-03-24 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_booking_user_booking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='booked',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
