# Generated by Django 4.0.3 on 2022-03-23 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0013_orderinstance_remove_orderline_due_back_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderInstance',
        ),
    ]
