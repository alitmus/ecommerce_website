# Generated by Django 4.2.5 on 2023-09-23 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_order_items_alter_orderitem_ordered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categories/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='label',
            field=models.CharField(choices=[('warning', 'new'), ('danger', 'sale'), ('info', 'bestseller'), ('success', 'season')], max_length=9),
        ),
    ]
