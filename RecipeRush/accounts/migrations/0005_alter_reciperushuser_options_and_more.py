# Generated by Django 4.2.3 on 2023-07-31 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_reciperushuser_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reciperushuser',
            options={},
        ),
        migrations.RemoveField(
            model_name='reciperushuser',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='reciperushuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='reciperushuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='reciperushuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='reciperushuser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='reciperushuser',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='reciperushuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='reciperushuser',
            name='user_permissions',
        ),
    ]
