# Generated by Django 5.1.2 on 2024-11-12 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_application_category_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='application/'),
        ),
    ]
