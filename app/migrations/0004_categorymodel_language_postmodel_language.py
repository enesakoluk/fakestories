# Generated by Django 4.0.3 on 2022-04-06 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_postmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='language',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='postmodel',
            name='language',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]