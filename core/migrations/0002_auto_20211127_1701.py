# Generated by Django 3.2.9 on 2021-11-27 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='message_by',
            new_name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='core.post'),
            preserve_default=False,
        ),
    ]
