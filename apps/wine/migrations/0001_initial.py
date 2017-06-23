# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 15:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_auto_20170623_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='WineInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, verbose_name='交易代码')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('winery', models.CharField(default='', max_length=64, verbose_name='酒庄')),
                ('proposed_price', models.FloatField(verbose_name='参考价格')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否无效酒')),
            ],
            options={
                'db_table': 'wine_info',
            },
        ),
        migrations.CreateModel(
            name='WineTradeOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commissioned_price', models.FloatField(verbose_name='委托价格')),
                ('trade_price', models.FloatField(verbose_name='交易价格')),
                ('trade_status', models.IntegerField(choices=[(0, '交易完成'), (1, '待交易')], default=1, verbose_name='交易状态')),
                ('commissioned_at', models.DateTimeField(auto_now_add=True, verbose_name='委托时间')),
                ('trade_at', models.DateTimeField(auto_now=True, verbose_name='交易时间')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='account.Jh_User')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='account.Jh_User')),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wine.WineInfo')),
            ],
        ),
    ]
