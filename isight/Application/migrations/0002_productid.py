# Generated by Django 3.1.4 on 2020-12-15 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Productid', models.CharField(max_length=200)),
            ],
        ),
    ]