# Generated by Django 3.2 on 2022-12-28 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_alter_customuser_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('Close Family', 'Close Family'), ('Family Around', 'Family Around'), ('Away Family', 'Away Family')], max_length=20)),
                ('kinship', models.CharField(choices=[('Mother', 'Mother'), ('Father', 'Father'), ('Brother', 'Brother'), ('Sister', 'Sister'), ('Wife', 'Wife'), ('Husband', 'Husband'), ('Cousin', 'Cousin'), ('Aunt', 'Aunt'), ('Uncle', 'Uncle'), ('Nephew', 'Nephew'), ('Niece', 'Niece'), ('Grandmother', 'Grandmother'), ('Grandfather', 'Grandfather'), ('Great-grandmother', 'Great-grandmother'), ('Great-grandfather', 'Great-grandfather'), ('Brother-in-law', 'Brother-in-law'), ('Sister-in-law', 'Sister-in-law'), ('Mother-in-law', 'Mother-in-law'), ('Father-in-law', 'Father-in-law')], max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('approved', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grp_name', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('familio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.familio')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]