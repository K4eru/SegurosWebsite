# Generated by Django 3.2.9 on 2021-11-25 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systemAuth', '0007_order_edited'),
    ]

    operations = [
        migrations.CreateModel(
            name='checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('professionalAssigned', models.IntegerField()),
                ('question1', models.CharField(max_length=100)),
                ('answer1', models.CharField(max_length=100)),
                ('question2', models.CharField(max_length=100)),
                ('answer2', models.CharField(max_length=100)),
                ('question3', models.CharField(max_length=100)),
                ('answer3', models.CharField(max_length=100)),
                ('question4', models.CharField(max_length=100)),
                ('answer4', models.CharField(max_length=100)),
                ('question5', models.CharField(max_length=100)),
                ('answer5', models.CharField(max_length=100)),
                ('orderID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extend', to='systemAuth.order')),
            ],
        ),
    ]