# Generated by Django 3.0.2 on 2020-09-11 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200911_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='datetime of email subscription')),
            ],
        ),
    ]