# Generated by Django 2.2.3 on 2020-07-13 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0039_auto_20200713_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='sign',
        ),
        migrations.AddField(
            model_name='shop',
            name='signs',
            field=models.ManyToManyField(blank=True, related_name='shop_sings', to='sushi_app.ShopSign'),
        ),
    ]
