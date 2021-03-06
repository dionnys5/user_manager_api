# Generated by Django 3.2.6 on 2021-08-06 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_customuser_last_login'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='first_name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='last_name',
            new_name='lastName',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
