# Generated by Django 3.1.4 on 2020-12-25 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0008_auto_20201225_0348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchingentry',
            options={'permissions': [('is_matcher', 'Can make matching suggestions'), ('is_moderator', 'Can moderate matching suggestions')], 'verbose_name_plural': 'Matching Entries'},
        ),
    ]