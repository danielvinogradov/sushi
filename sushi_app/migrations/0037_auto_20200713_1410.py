# Generated by Django 2.2.3 on 2020-07-13 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0036_requests_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopSign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Признак магазин',
                'verbose_name_plural': 'Признаки магазинов',
            },
        ),
        migrations.AddField(
            model_name='shop',
            name='sing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shop_sings', to='sushi_app.ShopSign'),
        ),
    ]