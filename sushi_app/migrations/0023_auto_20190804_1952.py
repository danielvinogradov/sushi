# Generated by Django 2.2.3 on 2019-08-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0022_auto_20190804_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='responsibles',
            field=models.ManyToManyField(limit_choices_to={'is_manager': True}, related_name='shop_responsible', to='sushi_app.UserProfile'),
        ),
    ]
