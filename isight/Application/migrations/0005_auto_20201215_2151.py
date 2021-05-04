# Generated by Django 3.1.4 on 2020-12-15 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0004_auto_20201215_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productid',
            name='userid',
        ),
        migrations.AddField(
            model_name='customerproduct',
            name='customerid',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Application.productid'),
        ),
    ]
