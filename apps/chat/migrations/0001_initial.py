# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wine', '0002_auto_20170627_1116'),
        ('account', '0004_auto_20170627_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=255, verbose_name='消息内容')),
                ('type', models.IntegerField(choices=[(0, '文本'), (1, '图片'), (2, '语音'), (3, '视频')], default=0, verbose_name='状态')),
                ('create_at', models.IntegerField(verbose_name='时间戳')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Jh_User')),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wine.WineInfo')),
            ],
            options={
                'db_table': 'chat_comments',
            },
        ),
    ]