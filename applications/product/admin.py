from django.contrib import admin
from applications.product.models import Product, ProductImage


class InlineProductImage(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image']

class ProductAdminDisplay(admin.ModelAdmin):
    inlines = [InlineProductImage, ]
    # fields = ['title,', 'price']

admin.site.register(Product, ProductAdminDisplay)
# admin.site.register(ProductImage, )
