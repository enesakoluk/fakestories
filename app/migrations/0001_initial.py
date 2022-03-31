# Generated by Django 4.0.3 on 2022-03-31 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, max_length=200, null=True)),
                ('stream', models.IntegerField(db_index=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isVideo', models.BooleanField(db_index=True)),
                ('link', models.URLField(blank=True)),
                ('stream', models.IntegerField(db_index=True, default=0)),
                ('title', models.TextField(blank=True, max_length=400, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('category', models.ManyToManyField(related_name='category_related', to='app.categorymodel')),
                ('favori', models.ManyToManyField(blank=True, related_name='favori_related', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, db_index=True, related_name='like_related', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]