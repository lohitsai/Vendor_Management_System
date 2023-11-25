# Generated by Django 4.2.6 on 2023-11-25 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrderModel',
            fields=[
                ('po_number', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField()),
                ('delivery_date', models.DateTimeField()),
                ('items', models.JSONField(default={})),
                ('quantity', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=10)),
                ('quality_rating', models.FloatField(blank=True, null=True)),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('acknowledgement_date', models.DateTimeField(blank=True, null=True)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.vendormodel')),
            ],
        ),
    ]
