# Generated by Django 3.2.13 on 2022-06-28 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_post_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
