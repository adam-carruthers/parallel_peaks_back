# Generated by Django 3.1.4 on 2020-12-25 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matching', '0007_auto_20201221_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchingentry',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='matching_entry', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]