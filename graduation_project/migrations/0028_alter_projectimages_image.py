# Generated by Django 4.2.18 on 2025-03-09 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation_project', '0027_projectimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='project_images'),
        ),
    ]
