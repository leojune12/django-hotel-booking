# Generated by Django 3.1.1 on 2020-10-02 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='reference_number',
            field=models.CharField(default='00000000', max_length=8),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_number',
            field=models.CharField(default='00000000', max_length=8),
        ),
    ]
