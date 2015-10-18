from functools import partial

from django import forms


class PartialMixin(object):

    @classmethod
    def partial(cls, *args, **kwargs):
        return partial(cls, *args, **kwargs)


class AuthorMixin(object):
    def save(self, *args, **kwargs):
        if self.instance.pk:
            self.instance.modified_by = self.user
        else:
            self.instance.created_by = self.user
        return super(AuthorMixin, self).save(*args, **kwargs)


class GIODOMixin(object):

    def __init__(self, *args, **kwargs):
        from tinycontent.models import TinyContent
        super(GIODOMixin, self).__init__(*args, **kwargs)
        self.fields['giodo'] = forms.BooleanField(required=True)
        try:
            self.fields['giodo'].label = TinyContent.get_content_by_name('giodo').content
        except TinyContent.DoesNotExist:
            self.fields['giodo'].label = 'Lorem ipsum'
