from django.contrib import admin
from .models import Category, Tag, Manufacturer

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    preserve_filters = {'slug' : ('name',)}

admin.site.register(Tag, TagAdmin)

class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Manufacturer, ManufacturerAdmin)