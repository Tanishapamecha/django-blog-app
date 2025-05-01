from django.apps import AppConfig

class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        import blog.signals  # This will import the signals when the app is ready
