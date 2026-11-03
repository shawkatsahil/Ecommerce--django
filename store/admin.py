from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "available"]
    list_filter = ["category", "available"]
    list_editable = ["price", "stock", "available"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
# Register your models here.
