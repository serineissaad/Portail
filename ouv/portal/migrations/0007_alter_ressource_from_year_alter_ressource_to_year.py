# Generated by Django 5.0.2 on 2024-02-24 23:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_alter_bd_reliee_annee_alter_bd_reliee_auteur_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ressource',
            name='from_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1950), django.core.validators.MaxValueValidator(2050)]),
        ),
        migrations.AlterField(
            model_name='ressource',
            name='to_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1950), django.core.validators.MaxValueValidator(2050)]),
        ),
    ]
