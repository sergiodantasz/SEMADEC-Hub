# Generated by Django 5.0.6 on 2024-05-28 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documents', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='collection',
            field=models.ForeignKey(db_column='collection_id', on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='home.collection'),
        ),
    ]
