from functools import partial

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Reset, Submit
from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l


class FormsetHelper(FormHelper):
    form_tag = False
    form_method = 'post'


class TableFormSetHelper(FormsetHelper):

    def __init__(self, *args, **kwargs):
        super(TableFormSetHelper, self).__init__(*args, **kwargs)
        self.template = 'bootstrap/table_inline_formset.html'


class BaseTableFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseTableFormSet, self).__init__(*args, **kwargs)
        self.helper = TableFormSetHelper()


class HelperMixin(object):
    form_helper_cls = FormHelper

    def __init__(self, *args, **kwargs):
        super(HelperMixin, self).__init__(*args, **kwargs)
        self.helper = getattr(self, 'helper', self.form_helper_cls(self))


class SingleButtonMixin(HelperMixin):
    form_helper_cls = FormHelper

    @property
    def action_text(self):
        return _('Update') if hasattr(self, 'instance') and self.instance.pk else _('Save')

    def __init__(self, *args, **kwargs):
        super(SingleButtonMixin, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('action', self.action_text, css_class="btn-primary"))


class SaveButtonMixin(SingleButtonMixin):

    def __init__(self, *args, **kwargs):
        super(SaveButtonMixin, self).__init__(*args, **kwargs)
        self.helper.add_input(Reset('reset', _('Reset!')))


class FormHorizontalMixin(HelperMixin):

    def __init__(self, *args, **kwargs):
        super(FormHorizontalMixin, self).__init__(*args, **kwargs)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'


class PartialMixin(object):

    @classmethod
    def partial(cls, *args, **kwargs):
        return partial(cls, *args, **kwargs)


class AuthorMixin(object):

    def save(self, commit=True, *args, **kwargs):
        obj = super(AuthorMixin, self).save(commit=False, *args, **kwargs)
        if obj.pk:  # update
            obj.modified_by = self.user
        else:  # new
            obj.created_by = self.user
        if commit:
            obj.save()
        return obj


class GIODOMixin(object):

    def __init__(self, *args, **kwargs):
        from tinycontent.models import TinyContent
        super(GIODOMixin, self).__init__(*args, **kwargs)
        self.fields['giodo'] = forms.BooleanField(required=True)
        try:
            self.fields['giodo'].label = TinyContent.get_content_by_name('giodo').content
        except TinyContent.DoesNotExist:
            self.fields['giodo'].label = 'Lorem ipsum'
