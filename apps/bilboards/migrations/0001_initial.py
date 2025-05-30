# Generated by Django 5.2 on 2025-05-15 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Manzil nomi')),
            ],
            options={
                'verbose_name': 'Manzil',
                'verbose_name_plural': 'Manzillar',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Viloyat nomi')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='bilboards.location', verbose_name='Manzil')),
            ],
            options={
                'verbose_name': 'Viloyat',
                'verbose_name_plural': 'Viloyatlar',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Tuman nomi')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='bilboards.region', verbose_name='Viloyat')),
            ],
            options={
                'verbose_name': 'Tuman',
                'verbose_name_plural': 'Tumanlar',
            },
        ),
        migrations.CreateModel(
            name='Billboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='billboard_images/', verbose_name='Rasm')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Lokatsiya manzili')),
                ('latitude', models.FloatField(verbose_name='Latitude (kenglik)')),
                ('longitude', models.FloatField(verbose_name='Longitude (uzunlik)')),
                ('billboard_number', models.CharField(max_length=50, verbose_name='Billboard raqami')),
                ('format', models.CharField(max_length=50, verbose_name='Format (masalan: 15FT)')),
                ('status', models.CharField(choices=[('free', 'Свободен'), ('occupied', 'Занят')], default='free', max_length=10, verbose_name='Status')),
                ('client', models.CharField(blank=True, max_length=255, null=True, verbose_name='Mijoz')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Narxi')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='Ijara tugash sanasi')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Umumiy summa')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqti')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilboards.district', verbose_name='Tuman')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilboards.location', verbose_name='Manzil')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilboards.region', verbose_name='Viloyat')),
            ],
            options={
                'verbose_name': 'Billboard',
                'verbose_name_plural': 'Billboardlar',
            },
        ),
    ]
