# Generated by Django 5.2.1 on 2025-07-07 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neural', '0018_productlistcards'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChartFileUploaderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorical_label', models.CharField(max_length=50)),
                ('data_label_numeric', models.FloatField()),
                ('data_numeric', models.FloatField()),
            ],
        ),
    ]
