# Generated by Django 2.1 on 2018-08-14 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alfa', '0002_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='alias',
            field=models.CharField(default='', max_length=100),
        ),
    ]