# Generated by Django 3.2.9 on 2021-12-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/default.jpg', upload_to='profile_images/'),
        ),
    ]
