# Generated by Django 5.1.4 on 2024-12-09 05:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_remove_patient_medic_info_patient_prescriptions'),
        ('prescriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescription_set', to='patients.patient'),
        ),
    ]
