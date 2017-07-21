from django.core.management.base import BaseCommand
from django.apps import apps
from itertools import groupby

class Command(BaseCommand):
    help = "A generator of serializer templates for 'djangorestframework' package"
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

        for model in models:
            self.process_model(model)

    def print_all_imports(self, models):
        all_imports = {my_import for model in models for my_import in self.generate_imports(model)}
        all_imports = sorted(all_imports, reverse=True)
        for module_name, class_names in groupby(all_imports, key=lambda x: x[0]):
            self.stdout.write("from {} import {}".format(module_name, ", ".join(x[1] for x in class_names)))

    def generate_imports(self, model):
        yield ('rest_framework', 'serializers')
        yield '.models', "{}".format(model.__name__)
        for field in model._meta.fields:
            if field.is_relation and field.model._meta.app_label != field.related_model._meta.app_label:
                module_name = field.related_model.__module__
                if module_name == field.model.__module__:
                    module_name = ".models"
                model_name = field.related_model.__name__

                serialize_module = module_name.replace('.models', '.serializers')
                class_name = model_name + "Serializer"
                yield serialize_module, class_name

    def print_file_header(self):
        pass

    def process_model(self, model):

        self.stdout.write("\n\nclass {}Serializer(serializers.HyperlinkedModelSerializer):\n".format(model.__name__))
        for attname, field in model._meta.fields_map.items():  # reverse foreign key
            args = 'many=True' if field.many_to_many or field.one_to_many else ''
            model_name = field.related_model.__name__
            self.stdout.write(self.INDENT + "{} = {}Serializer({})".format(attname, model_name, args))

        for field in model._meta.fields:
            if field.is_relation:
                # import ipdb; ipdb.set_trace();
                attname = field.attname.replace("_id", '')
                model_name = field.related_model.__name__
                args = 'many=True' if field.many_to_many else ''

                self.stdout.write(self.INDENT + "{} = {}Serializer({})".format(attname, model_name, args))

        self.stdout.write("\n")
        self.stdout.write(self.INDENT + "class Meta:")
        self.stdout.write(self.INDENT*2 + "model = {}".format(model.__name__))
        names = [x.attname.replace('_id', '') for x in model._meta.fields]
        self.stdout.write(self.INDENT*2 + "fields = {}".format(str(names)))