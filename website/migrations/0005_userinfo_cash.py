# Generated by Django 4.0.5 on 2022-07-07 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_delete_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='cash',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
