# Generated by Django 5.2.4 on 2025-07-23 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testy', '0005_testcategory_testquestion_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestQuestion',
        ),
    ]
