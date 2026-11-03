from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["image_preview", "name", "category", "price", "stock", "available"]
    list_display_links = ["name"]
    list_filter = ["category", "available"]
    list_editable = ["price", "stock", "available"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="object-fit: cover; border-radius: 6px;">',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Image"
# Register your models here.
