# Generated by Django 5.0.6 on 2024-05-20 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostic', '0002_remove_devis_garage'),
    ]

    operations = [
        migrations.AddField(
            model_name='devis',
            name='total_prix',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
