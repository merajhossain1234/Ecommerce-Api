from django.contrib import admin
from .models import Profile, Category, Product,Cart,CartProduct,Order

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'prouser', 'image']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date', 'category', 'market_price', 'selling_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total', 'completed', 'date']


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'get_product_title', 'price', 'quantity', 'subtotal']

    def get_product_title(self, obj):
        return obj.product.title

    get_product_title.short_description = 'Product Title'
    
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'address', 'mobile', 'email', 'total', 'discount', 'order_status', 'date', 'payment']