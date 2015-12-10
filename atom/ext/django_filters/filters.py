import django_filters
from django.utils.translation import ugettext_lazy as _

I18n_ORDERING = _("Ordering")


class CrispyFilterMixin(object):
    form_class = 'form-inline'

    @property
    def form(self):
        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Submit
        self._form = super(CrispyFilterMixin, self).form
        self._form.helper = FormHelper(self._form)
        if self.form_class:
            self._form.helper.form_class = 'form-inline'
        self._form.helper.form_method = 'get'
        self._form.helper.layout.append(Submit('filter', _('Filter')))
        return self._form


class AutocompleteChoiceFilter(django_filters.ModelChoiceFilter):

    def __init__(self, autocomplete_name, *args, **kwargs):
        from autocomplete_light import shortcuts as autocomplete_light
        autocomplete = autocomplete_light.registry.get_autocomplete_from_arg(autocomplete_name)
        if 'label' not in kwargs:
            kwargs['label'] = autocomplete.model._meta.verbose_name
        kwargs['queryset'] = autocomplete.choices
        kwargs['widget'] = autocomplete_light.ChoiceWidget(autocomplete)
        super(AutocompleteChoiceFilter, self).__init__(*args, **kwargs)


class UserKwargFilterSetMixin(object):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserKwargFilterSetMixin, self).__init__(*args, **kwargs)
