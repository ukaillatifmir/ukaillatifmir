# Generated by Django 3.1.5 on 2021-08-06 07:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to='')),
                ('discription', models.CharField(blank=True, max_length=300)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2021, 8, 6, 12, 51, 9, 636862))),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_name', models.CharField(blank=True, max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20)),
                ('Gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], max_length=20)),
                ('Email', models.EmailField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('login_successful', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2021, 8, 6, 12, 51, 9, 635864))),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('link', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='master.cover')),
            ],
        ),
        migrations.AddField(
            model_name='cover',
            name='email',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='master.user'),
        ),
        migrations.CreateModel(
            name='business_card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='master.user', unique=True)),
            ],
        ),
    ]
