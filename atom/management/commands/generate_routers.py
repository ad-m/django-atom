from django.core.management.base import BaseCommand
from django.apps import apps
from itertools import groupby


class Command(BaseCommand):
    help = "A generator of router templates for 'djangorestframework' package"
    INDENT = " "*4

    def add_arguments(self, parser):
        parser.add_argument('app_label')
        parser.add_argument('model_name', help="Use '__all__' as all models of app")

    def handle(self, app_label, model_name, *args, **options):
        if model_name in ['-a', '__all__']:
            models = list(apps.get_app_config(app_label).get_models())
        else:
            models = [apps.get_app_config(app_label).get_model(model_name)]

        try:
            from rest_framework import serializers
        except ImportError:
            self.stdout.write("The 'djangorestframework' package is not installed. The generated "
                              "code will not work properly without this.")
        self.print_file_header()

        self.print_all_imports(models)

        self.stdout.write("\n\nrouter = routers.DefaultRouter()")
        for model in models:
            self.process_model(model)

    def print_all_imports(self, models):
        all_imports = {my_import for model in models for my_import in self.generate_imports(model)}
        all_imports = sorted(all_imports, reverse=True)
        for module_name, class_names in groupby(all_imports, key=lambda x: x[0]):
            self.stdout.write("from {} import {}".format(module_name, ", ".join(x[1] for x in class_names)))

    def generate_imports(self, model):
        yield 'rest_framework', 'routers'
        yield model.__package__, "{}ViewSet".format(model.__name__)

    def print_file_header(self):
        pass

    def process_model(self, model):
        app_label = model._meta.app_label
        model_name = model.__name__
        model_small = model.__name__.lower()
        self.stdout.write("router.register(r'{}/{}', {}ViewSet)".format(app_label, model_small, model_name))