# Generated by Django 4.2.5 on 2023-10-17 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_suppliers_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='phone_no',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='suppliers',
            name='phone_no',
            field=models.CharField(max_length=100),
        ),
    ]
