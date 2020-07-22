# Generated by Django 2.2.7 on 2020-07-22 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20200722_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='text_kg',
            field=models.TextField(null=True, verbose_name='Текст'),
        ),
        migrations.AddField(
            model_name='article',
            name='text_ru',
            field=models.TextField(null=True, verbose_name='Текст'),
        ),
        migrations.AddField(
            model_name='article',
            name='title_kg',
            field=models.CharField(max_length=100, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='article',
            name='title_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='articleaddition',
            name='subtext_kg',
            field=models.TextField(null=True, verbose_name='Подтекст'),
        ),
        migrations.AddField(
            model_name='articleaddition',
            name='subtext_ru',
            field=models.TextField(null=True, verbose_name='Подтекст'),
        ),
        migrations.AddField(
            model_name='articleaddition',
            name='subtitle_kg',
            field=models.CharField(max_length=100, null=True, verbose_name='Подзаголовок'),
        ),
        migrations.AddField(
            model_name='articleaddition',
            name='subtitle_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Подзаголовок'),
        ),
    ]
