from django.contrib import admin

from .models import Product, LikeProduct, ProductPhoto

admin.site.register(Product)
admin.site.register(LikeProduct)
admin.site.register(ProductPhoto)
