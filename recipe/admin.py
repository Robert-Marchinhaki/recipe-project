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
        'id',
        'title',
        'created_at',
        'is_published',
    ]
    list_display_links = [
        'title',
        'created_at',
    ]
    list_filter = [
        'author',
        'category',
        'created_at',
        'is_published',
        'preparation_step_is_html',
    ]
    search_fields = [
        'id',
        'title',
        'slug',
        'description',
    ]
    actions = [
        published_on,
        published_off,
    ]
    list_per_page = 10
    list_editable = [
        'is_published',
    ]
    ordering = [
        '-id',
    ]
    prepopulated_fields = {
        "slug": [
            "title",
        ],
    }

# admin.site.register(RecipeAdmin)
