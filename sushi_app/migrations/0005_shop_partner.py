# Generated by Django 2.2.2 on 2019-07-18 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sushi_app', '0004_customdocument_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='partner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
