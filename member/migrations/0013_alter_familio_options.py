# Generated by Django 3.2.16 on 2023-03-02 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0012_group_member'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='familio',
            options={'ordering': ['name']},
        ),
    ]
