# Generated by Django 2.0.7 on 2018-07-30 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20180730_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pending_messages',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
