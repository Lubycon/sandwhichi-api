# Generated by Django 2.0.6 on 2018-06-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20180622_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='contacts',
            field=models.ManyToManyField(to='common.Contact'),
        ),
        migrations.AlterField(
            model_name='project',
            name='media',
            field=models.ManyToManyField(to='common.Media'),
        ),
    ]