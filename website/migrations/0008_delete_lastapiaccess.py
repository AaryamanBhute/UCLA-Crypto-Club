# Generated by Django 4.0.5 on 2022-08-21 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_alter_lastapiaccess_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LastApiAccess',
        ),
    ]