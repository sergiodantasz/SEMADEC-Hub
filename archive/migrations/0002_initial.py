# Generated by Django 5.0.1 on 2024-02-01 14:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('archive', '0001_initial'),
        ('home', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='administrator',
            field=models.ForeignKey(db_column='administrator_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.administrator'),
        ),
        migrations.AddField(
            model_name='collection',
            name='tags',
            field=models.ManyToManyField(to='home.tag'),
        ),
        migrations.AddField(
            model_name='file',
            name='collection',
            field=models.ForeignKey(db_column='collection_id', on_delete=django.db.models.deletion.CASCADE, to='archive.collection'),
        ),
    ]
