# Generated by Django 2.0.6 on 2018-06-16 08:53

from django.db import migrations

def forwards_func(apps, schema_editor):
    ContactType = apps.get_model('common', 'ContactType')
    db_alias = schema_editor.connection.alias
    ContactType.objects.using(db_alias).bulk_create([
        ContactType(name='이메일'),
        ContactType(name='카카오 오픈채팅'),
        ContactType(name='카카오톡'),
        ContactType(name='페이스북'),
    ])
    
    MediaType = apps.get_model('common', 'MediaType')
    MediaType.objects.using(db_alias).bulk_create([
        MediaType(name='이미지'),
        MediaType(name='유튜브'),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
