# Generated by Django 2.2.3 on 2019-08-25 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0026_auto_20190825_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='position',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
