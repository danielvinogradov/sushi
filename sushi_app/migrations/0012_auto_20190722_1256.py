# Generated by Django 2.2.2 on 2019-07-22 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0011_auto_20190722_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='manager',
            field=models.ForeignKey(blank=True, limit_choices_to={'manager': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager', to='wagtailusers.UserProfile'),
        ),
    ]