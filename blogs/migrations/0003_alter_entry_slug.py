# Generated by Django 4.2.1 on 2023-05-31 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_entry_public_entry_slug_alter_topic_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]