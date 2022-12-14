# Generated by Django 4.0.6 on 2022-07-19 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.IntegerField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('subtext', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='thread',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='social.genre'),
        ),
    ]
