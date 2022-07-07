from django.contrib import admin

from .models import Category, Recipe


@admin.action(description="Aprovar publicação")
def published_on(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Desaprovar publicação")
def published_off(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_published',
        'created_at',
    ]
    list_filter = [
        'created_at',
        'preparation_step_is_html',
    ]
    actions = [
        published_on,
        published_off,
    ]


# admin.site.register(RecipeAdmin)
