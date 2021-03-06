# Generated by Django 2.2.2 on 2019-07-06 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('short_descrip', models.CharField(max_length=256)),
                ('descrip', models.TextField()),
                ('composition', models.TextField()),
                ('characteristics', models.TextField()),
                ('date_update', models.DateTimeField(auto_now=True, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(choices=[(1, 'Ужасно'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')], default=5)),
                ('files', models.ImageField(blank=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Messeges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('accepter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accepter', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_messeges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('adv', models.TextField()),
                ('disadv', models.TextField()),
                ('files', models.FileField(blank=True, null=True, upload_to='')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(choices=[(1, 'Ужасно'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')], default=5)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_feed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
