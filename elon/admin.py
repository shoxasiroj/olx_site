from django.contrib import admin
from .models import Elon, AdditionalImage


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class ElonAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'body', 'author', 'created_at']
    fields = (('category', 'author'), ('title', 'price'), 'body', 'country_code', 'image', 'is_active')
    inlines = (AdditionalImageInline,)


admin.site.register(Elon, ElonAdmin)
