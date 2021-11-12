# Generated by Django 3.2.7 on 2021-10-28 11:23

from django.db import migrations, models
import uploads.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160801_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='description',
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=uploads.core.models.only_filename),
        ),
    ]