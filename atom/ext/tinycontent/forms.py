from django import forms

from tinycontent.models import TinyContent


class GIODOMixin(object):
    def __init__(self, *args, **kwargs):
        super(GIODOMixin, self).__init__(*args, **kwargs)
        self.fields['giodo'] = forms.BooleanField(required=True)
        try:
            self.fields['giodo'].label = TinyContent.get_content_by_name('giodo').content
        except TinyContent.DoesNotExist:
            self.fields['giodo'].label = 'Lorem ipsum'
