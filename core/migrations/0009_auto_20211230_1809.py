# Generated by Django 3.2.9 on 2021-12-30 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_notification_user_has_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.comment'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.post'),
        ),
    ]
