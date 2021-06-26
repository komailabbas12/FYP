# Generated by Django 3.1.7 on 2021-05-28 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Application', '0021_ymlfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='videoStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoFile', models.FileField(null=True, upload_to='')),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]