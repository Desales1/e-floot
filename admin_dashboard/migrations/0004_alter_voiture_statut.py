# Generated by Django 5.0.6 on 2024-05-30 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0003_rename_garage_assigné_voiture_garage_assigne'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voiture',
            name='statut',
            field=models.CharField(choices=[('en attente de diagnostic', 'En attente de diagnostic'), ('diagnostiquée', 'Diagnostiquee')], default='en attente de diagnostic', max_length=30),
        ),
    ]