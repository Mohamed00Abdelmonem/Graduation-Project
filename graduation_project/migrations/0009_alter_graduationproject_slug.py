# Generated by Django 4.2.18 on 2025-01-20 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation_project', '0008_graduationproject_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduationproject',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
