# Generated by Django 3.2.8 on 2021-10-25 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemAuth', '0002_auto_20211025_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonusermodel',
            name='userRut',
            field=models.CharField(max_length=50),
        ),
    ]
