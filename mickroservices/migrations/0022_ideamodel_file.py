# Generated by Django 2.2.3 on 2019-10-13 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0021_merge_20190911_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideamodel',
            name='file',
            field=models.FileField(blank=True, upload_to='ideas'),
        ),
    ]