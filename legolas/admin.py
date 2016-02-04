from django.contrib import admin

from .models import Area, SubArea, Category, SubCategory, Store, Review, Comment



admin.site.register(Area)
admin.site.register(SubArea)
admin.site.register(Category)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['parent']

admin.site.register(SubCategory ,SubCategoryAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'area', 'sub_area']
    list_display_links = ['name']
    search_fields = ['name', 'intro', 'menu']

admin.site.register(Store, StoreAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'store', 'user_rating', 'created_at', 'n_like' ]

admin.site.register(Review, ReviewAdmin)


admin.site.register(Comment)

