# Generated by Django 2.2.7 on 2020-08-29 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0002_thread_times_rooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='messages/file/', verbose_name='Файл'),
        ),
    ]
