# Generated by Django 4.2.18 on 2025-03-29 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation_project', '0031_alter_graduationproject_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduationproject',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='projects/images/'),
        ),
    ]
