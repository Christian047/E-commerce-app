# Generated by Django 5.0.2 on 2024-02-26 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_payment_email_payment_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='email',
            field=models.EmailField(default=2, max_length=254),
            preserve_default=False,
        ),
    ]