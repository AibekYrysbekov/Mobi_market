from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(verbose_name='Название товара', max_length=255)
    description = models.TextField(verbose_name='Описание', max_length=500)
    short_description = models.CharField(verbose_name='Короткое описание', max_length=255)
    available = models.BooleanField(verbose_name="В наличии?", default=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукт'

    def __str__(self):
        return self.name


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Фото товара', upload_to='Mobi_market/media/product_image',
                              default='product_image/product.png', null=True, blank=True)

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фотографии продукта'


class LikeProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    like = models.BooleanField(verbose_name='Понравившийся товар', default=False)

    class Meta:
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайк'

    def __str__(self):
        return f"{self.product}"
