# Generated by Django 4.2.18 on 2025-03-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation_project', '0028_alter_projectimages_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graduationproject',
            old_name='images',
            new_name='main_image',
        ),
        migrations.AddField(
            model_name='graduationproject',
            name='pages_image',
            field=models.ImageField(blank=True, null=True, upload_to='projects/pages_image/'),
        ),
        migrations.AlterField(
            model_name='graduationproject',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
        migrations.DeleteModel(
            name='ProjectImages',
        ),
    ]
