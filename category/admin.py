from django.contrib import admin
from .models import SuperCategory, ChildCategory
from .forms import ChildCategoryForm


# admin.site.register(SuperCategory)
# admin.site.register(ChildCategory)


class ChildCategoryInline(admin.TabularInline):
    model = ChildCategory


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('parent_category',)
    inlines = (ChildCategoryInline,)


class ChildCategoryAdmin(admin.ModelAdmin):
    form = ChildCategoryForm


admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(ChildCategory, ChildCategoryAdmin)
