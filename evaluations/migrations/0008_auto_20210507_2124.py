# Generated by Django 3.1 on 2021-05-08 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0007_auto_20210507_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
