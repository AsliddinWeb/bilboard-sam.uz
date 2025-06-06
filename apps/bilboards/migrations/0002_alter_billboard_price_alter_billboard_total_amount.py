# Generated by Django 5.2 on 2025-05-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilboards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billboard',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Narxi'),
        ),
        migrations.AlterField(
            model_name='billboard',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Umumiy summa'),
        ),
    ]
