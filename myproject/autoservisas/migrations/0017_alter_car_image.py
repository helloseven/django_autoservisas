# Generated by Django 4.0.3 on 2022-03-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0016_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='img', verbose_name='Image'),
        ),
    ]
