# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20170627_1116'),
        ('wine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_direction', models.IntegerField(choices=[(0, '买入'), (1, '卖出')], default=1, verbose_name='买卖方向')),
                ('price', models.FloatField(verbose_name='委托价')),
                ('num', models.IntegerField(default=1, verbose_name='委托数量')),
                ('status', models.IntegerField(choices=[(0, '可撤'), (1, '已撤单'), (2, '已成交'), (3, '取消')], default=0, verbose_name='状态')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='委托时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Jh_User')),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wine.WineInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='成交价')),
                ('num', models.IntegerField(default=1, verbose_name='成交数量')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='成交时间')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='account.Jh_User')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='account.Jh_User')),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wine.WineInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='开仓价')),
                ('num', models.IntegerField(default=1, verbose_name='持仓量')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Jh_User')),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wine.WineInfo')),
            ],
        ),
        migrations.RemoveField(
            model_name='winetradeorder',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='winetradeorder',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='winetradeorder',
            name='wine',
        ),
        migrations.DeleteModel(
            name='WineTradeOrder',
        ),
    ]
