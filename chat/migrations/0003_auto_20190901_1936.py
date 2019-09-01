# Generated by Django 2.2.3 on 2019-09-01 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0028_auto_20190826_1439'),
        ('chat', '0002_auto_20190831_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='feedback',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Feedback'),
        ),
        migrations.AddField(
            model_name='message',
            name='requests',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Requests'),
        ),
        migrations.AddField(
            model_name='message',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Task'),
        ),
    ]
