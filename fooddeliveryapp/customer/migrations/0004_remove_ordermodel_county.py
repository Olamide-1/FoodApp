# Generated by Django 2.1.1 on 2022-12-07 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20221207_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='county',
        ),
    ]
