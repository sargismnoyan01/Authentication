# Generated by Django 5.1.2 on 2024-12-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_myuser_age_myuser_gender_myuser_img_myuser_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Product name')),
                ('img', models.ImageField(upload_to='products', verbose_name='image')),
                ('price', models.IntegerField(verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
