# Generated by Django 3.0.5 on 2020-04-02 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Review',
            new_name='Reviewmodel',
        ),
        migrations.RenameModel(
            old_name='Shelf',
            new_name='Shelfmodel',
        ),
    ]
