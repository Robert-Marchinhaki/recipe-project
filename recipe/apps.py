from django.apps import AppConfig


class RecipeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipe'

    def ready(self, *args, **kwargs) -> None:
        import recipe.signals  # noqa
        super_ready = super().ready(*args, **kwargs)
        return super_ready
