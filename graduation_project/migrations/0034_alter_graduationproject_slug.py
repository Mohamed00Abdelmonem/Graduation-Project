# Generated by Django 4.2.18 on 2025-05-26 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation_project', '0033_graduationproject_audio_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduationproject',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
