from django.apps import AppConfig
from django.template.context import Context, RequestContext


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        def safe_copy(self):
            if isinstance(self, RequestContext):
                duplicate = self.__class__(self.request)
            else:
                duplicate = self.__class__()
            duplicate.dicts = list(self.dicts)
            return duplicate

        Context.__copy__ = safe_copy
        RequestContext.__copy__ = safe_copy
