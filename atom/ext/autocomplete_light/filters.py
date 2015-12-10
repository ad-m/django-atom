import django_filters
from autocomplete_light import shortcuts as autocomplete_light


class AutocompleteChoiceFilter(django_filters.ModelChoiceFilter):
    def __init__(self, autocomplete_name, *args, **kwargs):
        autocomplete = autocomplete_light.registry.get_autocomplete_from_arg(autocomplete_name)
        kwargs['queryset'] = autocomplete.choices
        kwargs['widget'] = autocomplete_light.ChoiceWidget(autocomplete)
        super(AutocompleteChoiceFilter, self).__init__(*args, **kwargs)
