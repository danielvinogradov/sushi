# Generated by Django 2.2.2 on 2019-07-06 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0002_auto_20190706_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionmodel',
            name='phone_number',
            field=models.CharField(default=0, max_length=12, verbose_name='Номер телефона'),
            preserve_default=False,
        ),
    ]
