# Generated by Django 4.2.6 on 2023-11-25 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0002_alter_purchaseordermodel_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseordermodel',
            name='acknowledged',
            field=models.BooleanField(auto_created=True, default=False),
        ),
    ]
