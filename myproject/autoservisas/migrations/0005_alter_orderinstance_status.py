# Generated by Django 4.0.3 on 2022-03-17 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0004_alter_service_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinstance',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'None'), (1, 'Accepted'), (2, 'Fixed'), (3, 'Declined')], db_index=True, default=0, verbose_name='Status'),
        ),
    ]