# Generated by Django 4.2.18 on 2025-03-05 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_userprofile_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='full_name',
        ),
    ]
