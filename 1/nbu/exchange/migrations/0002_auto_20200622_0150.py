# Generated by Django 2.0.13 on 2020-06-21 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='exchange',
            unique_together={('exchangedate', 'cc')},
        ),
    ]