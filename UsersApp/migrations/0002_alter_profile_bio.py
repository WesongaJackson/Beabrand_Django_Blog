# Generated by Django 4.2.2 on 2023-06-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]