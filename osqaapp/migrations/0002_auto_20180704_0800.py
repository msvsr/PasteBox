# Generated by Django 2.0.5 on 2018-07-04 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osqaapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alike',
            name='like',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='qlike',
            name='like',
            field=models.IntegerField(default=1),
        ),
    ]
