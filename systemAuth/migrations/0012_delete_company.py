# Generated by Django 4.0 on 2021-12-12 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('systemAuth', '0011_alter_commonusermodel_company'),
    ]

    operations = [
        migrations.DeleteModel(
            name='company',
        ),
    ]
