# Generated by Django 5.1.6 on 2025-03-26 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_otherannouncement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otherannouncement',
            options={'verbose_name': 'Другое объявление', 'verbose_name_plural': 'Другие объявления'},
        ),
    ]
