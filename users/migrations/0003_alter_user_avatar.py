# Generated by Django 5.0 on 2023-12-25 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='user_image/avatar.png', null=True, upload_to='Mobi_market/media/user_image'),
        ),
    ]