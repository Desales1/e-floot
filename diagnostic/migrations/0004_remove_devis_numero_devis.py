# Generated by Django 5.0.6 on 2024-05-20 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostic', '0003_devis_total_prix'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devis',
            name='numero_devis',
        ),
    ]