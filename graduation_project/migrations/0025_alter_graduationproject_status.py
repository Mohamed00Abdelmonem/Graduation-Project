# Generated by Django 4.2.18 on 2025-03-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation_project', '0024_alter_graduationproject_graduation_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduationproject',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('temporary_rejection', 'Temporary_Rejection')], db_index=True, default='pending', max_length=20),
        ),
    ]
