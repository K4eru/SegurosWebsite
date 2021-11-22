# Generated by Django 3.2.9 on 2021-11-21 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('systemAuth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commonusermodel',
            old_name='userFirstName',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='commonusermodel',
            old_name='userLastName',
            new_name='lastName',
        ),
        migrations.RenameField(
            model_name='commonusermodel',
            old_name='userPhoneNumber',
            new_name='phoneNumber',
        ),
        migrations.RenameField(
            model_name='commonusermodel',
            old_name='userRut',
            new_name='rut',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='userAddress',
            new_name='address',
        ),
    ]
