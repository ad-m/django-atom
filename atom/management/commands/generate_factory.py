from django.core.management.base import BaseCommand
from django.db import models
from django.apps import apps

class Command(BaseCommand):
    help = "A generator of factory templates for 'factory_boy' package"
    BASE_CLASS = "factory.django.DjangoModelFactory"
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
            import factory
        except ImportError:
            self.stdout.write("The 'factory-boy' package is not installed. The generated "
                              "code will not work properly without this.")
        self.print_file_header()

        for my_import in {my_import for model in models for my_import in self.print_imports(model)}:
            self.stdout.write(my_import)

        for model in models:
            self.print_class_header(model)
            self.process_fields(model)
            self.print_footer(app_label, model)

    def print_class_header(self, model):
        subfactory_name = self.get_subfactory_name(model)
        self.stdout.write("\n\nclass {}({}):".format(subfactory_name, self.BASE_CLASS))

    def print_field(self, definition, name):
        self.stdout.write(self.INDENT + "{} = {}".format(name, definition))

    def process_fields(self, model):
        for field in model._meta.fields:
            name = field.attname
            if isinstance(field, models.ForeignKey):  # ForeignKey field have suffix "_id"
                name = name.replace('_id', '')
            definition = self.get_creator_for_field(name, field, model)
            if definition:
                self.print_field(definition, name)

    def get_subfactory_name(self, model):
        return "{}Factory".format(model.__name__)

    def get_subfactory_path(self, related_model):
        path = related_model.__module__.replace('.models', '.tests.factories')
        name = self.get_subfactory_name(related_model)
        return "{}.{}".format(path, name)

    def get_creator_for_field(self, name, field, model):
        if isinstance(field, models.AutoField):
            return False
        if isinstance(field, models.ForeignKey):
            return 'factory.SubFactory("{}")'.format(self.get_subfactory_path(field.related_model))
        if isinstance(field, models.CharField):
            return 'factory.Sequence("{0}-{1}-{{0}}".format)'.format(self.safe_name(model.__name__), self.safe_name(name))
        if isinstance(field, models.TextField):
            return "factory.fuzzy.FuzzyText()"
        if isinstance(field, (models.BooleanField, models.NullBooleanField)):
            return "factory.Sequence(lambda n: n % 2 == 0)"
        if isinstance(field, (models.IntegerField, models.SmallIntegerField)):
            return "factory.Sequence(lambda n: n)"
        if isinstance(field, (models.DateTimeField)):
            if field.__class__.__name__ in ['AutoLastModifiedField', 'AutoCreatedField']:  # django-model-utils fields
                return False
            return "factory.fuzzy.FuzzyNaiveDateTime(datetime.datetime(2008, 1, 1))"
        return "UNKNOWN  # TODO: {}".format(field.__class__.__name__)

    def safe_name(self, text):
        return text.lower()

    def print_file_header(self):
        return self.stdout.write("# coding=utf-8")

    def print_imports(self, model):
        imports = {"import factory", "import factory.fuzzy"}
        for field in model._meta.fields:
            if not isinstance(field, models.ForeignKey):
                continue
            related_model = field.related_model
            if model.__module__ == related_model.__module__:
                continue
            module_path = related_model.__module__.replace('.models', '.factories')
            subfactory_name = self.get_subfactory_name(related_model)
            imports.add("from {} import {}".format(module_path, subfactory_name))
        return imports

    def print_footer(self, app_label, model):
        self.stdout.write("\n" +
                          self.INDENT + "class Meta:\n" +
                          self.INDENT*2 + "model = '{}.{}'".format(app_label, model.__name__))
