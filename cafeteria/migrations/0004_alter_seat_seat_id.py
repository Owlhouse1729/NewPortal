# Generated by Django 4.0.6 on 2022-07-24 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteria', '0003_remove_seat_column_remove_seat_date_remove_seat_row_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='seat_id',
            field=models.IntegerField(null=True),
        ),
    ]
