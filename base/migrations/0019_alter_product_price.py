# Generated by Django 5.0.6 on 2024-05-27 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_product_favorite_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=200),
        ),
    ]