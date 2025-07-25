# Generated by Django 5.2.4 on 2025-07-23 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testy', '0006_delete_testquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcategory',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('a', models.CharField(max_length=255)),
                ('b', models.CharField(max_length=255)),
                ('c', models.CharField(max_length=255)),
                ('d', models.CharField(max_length=255)),
                ('correct', models.CharField(max_length=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testy.testcategory')),
            ],
        ),
    ]
