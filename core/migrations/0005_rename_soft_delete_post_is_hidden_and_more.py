# Generated by Django 4.1.7 on 2023-03-25 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_post_deleted_at_post_soft_delete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='soft_delete',
            new_name='is_hidden',
        ),
        migrations.RemoveField(
            model_name='post',
            name='deleted_at',
        ),
    ]
