# Generated by Django 4.2.18 on 2025-02-11 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graduation_project', '0015_graduationproject_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graduationproject',
            name='author',
        ),
    ]
