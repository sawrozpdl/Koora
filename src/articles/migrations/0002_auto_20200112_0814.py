# Generated by Django 3.0.2 on 2020-01-12 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(blank=True, choices=[('RN', 'RANDOM'), ('SC', 'SCIENCE'), ('TG', 'TECHNOLOGY'), ('FD', 'FOOD'), ('AR', 'ART'), ('LT', 'LITERATURE'), ('PH', 'PHILOSOPHY'), ('MM', 'MUSIC&MOVIES'), ('TS', 'TVSERIES'), ('GM', 'GAMES')], default='RN', max_length=2),
        ),
    ]
