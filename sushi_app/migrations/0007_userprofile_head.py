# Generated by Django 2.2.2 on 2019-07-19 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0006_auto_20190718_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='sushi_app.UserProfile'),
        ),
    ]
