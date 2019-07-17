# Generated by Django 2.2.2 on 2019-07-17 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0004_auto_20190717_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingMaterial',
            fields=[
                ('texttemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mickroservices.TextTemplate')),
            ],
            options={
                'verbose_name': 'Маркетинговые материалы',
            },
            bases=('mickroservices.texttemplate',),
        ),
    ]