# Generated by Django 3.2.16 on 2023-03-01 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_alter_familio_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familio',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, null=True),
        ),
    ]
