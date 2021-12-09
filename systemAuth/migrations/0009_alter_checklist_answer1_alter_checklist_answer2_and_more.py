# Generated by Django 4.0 on 2021-12-08 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemAuth', '0008_checklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='answer1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='answer2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='answer3',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='answer4',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='answer5',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='question1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='question2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='question3',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='question4',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='question5',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]