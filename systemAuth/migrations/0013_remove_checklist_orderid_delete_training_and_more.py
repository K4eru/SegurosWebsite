# Generated by Django 4.0 on 2021-12-13 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('systemAuth', '0012_delete_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='orderID',
        ),
        migrations.DeleteModel(
            name='training',
        ),
        migrations.DeleteModel(
            name='checklist',
        ),
        migrations.DeleteModel(
            name='order',
        ),
    ]