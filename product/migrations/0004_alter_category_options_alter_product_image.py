# Generated by Django 4.1.3 on 2022-12-20 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_category_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ManyToManyField(blank=True, to='product.productimage', verbose_name='images'),
        ),
    ]