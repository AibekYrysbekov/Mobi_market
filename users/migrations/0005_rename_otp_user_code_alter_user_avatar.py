# Generated by Django 5.0 on 2023-12-29 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='otp',
            new_name='code',
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='user_image/avatar.png', null=True, upload_to='Mobi_market/media/user_image'),
        ),
    ]
