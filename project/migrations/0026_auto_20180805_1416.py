# Generated by Django 2.0.6 on 2018-08-05 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_auto_20180805_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmemberrequest',
            name='status',
            field=models.CharField(choices=[('REQUESTED', 'Requested'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('CANCELED', 'Canceled')], max_length=10),
        ),
    ]
