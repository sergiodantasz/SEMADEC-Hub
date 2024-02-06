# Generated by Django 5.0.1 on 2024-02-06 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('excerpt', models.CharField(max_length=200)),
                ('cover', models.ImageField(default=None, upload_to='')),
                ('content', models.TextField()),
                ('slug', models.SlugField(max_length=225, unique=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(default=None)),
                ('administrator', models.ForeignKey(db_column='administrator_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.administrator')),
                ('tags', models.ManyToManyField(to='home.tag')),
            ],
        ),
    ]
