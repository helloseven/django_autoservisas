# Generated by Django 4.0.3 on 2022-03-21 18:29

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0007_alter_order_options_remove_orderinstance_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='description',
            field=tinymce.models.HTMLField(help_text='Short description of the car', max_length=1000, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='orderinstance',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_instance', to='autoservisas.order'),
        ),
    ]