import django_filters
from autocomplete_light import ChoiceWidget
from autocomplete_light.registry import registry


class AutocompleteChoiceFilter(django_filters.ModelChoiceFilter):
    def __init__(self, autocomplete_name, *args, **kwargs):
        autocomplete = registry.get_autocomplete_from_arg(autocomplete_name)
        kwargs['queryset'] = autocomplete.choices
        kwargs['widget'] = ChoiceWidget(autocomplete)
        super(AutocompleteChoiceFilter, self).__init__(*args, **kwargs)
