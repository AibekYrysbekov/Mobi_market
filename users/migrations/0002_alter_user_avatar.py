# Generated by Django 5.0 on 2023-12-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='product_image/avatar.png', null=True, upload_to='Mobi_market/media/user_image'),
        ),
    ]
