# Generated by Django 3.1.4 on 2020-12-21 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Application', '0014_auto_20201216_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='pdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pdfstore', models.FileField(null=True, upload_to='')),
                ('coverimage', models.FileField(null=True, upload_to='')),
                ('title', models.CharField(max_length=200)),
                ('desp', models.CharField(max_length=200)),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagestore', models.FileField(null=True, upload_to='')),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]