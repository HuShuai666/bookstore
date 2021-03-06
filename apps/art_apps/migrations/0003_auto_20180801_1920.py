# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-01 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('art_apps', '0002_auto_20180801_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='单价')),
                ('quantity', models.IntegerField(default=0, verbose_name='购买数量')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('flag', models.IntegerField(choices=[(0, '代下单'), (2, '已下单')], default=0, verbose_name='购买状态')),
            ],
            options={
                'verbose_name': '购物车条目',
                'verbose_name_plural': '购物车条目',
                'db_table': 'line_item',
            },
        ),
        migrations.AddField(
            model_name='arts',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=7, verbose_name='单价'),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='art_apps.Arts', verbose_name='小说产品'),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='art_apps.Users', verbose_name='购买用户'),
        ),
    ]
