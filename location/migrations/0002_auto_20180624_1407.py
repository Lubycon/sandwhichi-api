# Generated by Django 2.0.6 on 2018-06-24 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
