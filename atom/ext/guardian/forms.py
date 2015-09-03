from django.utils.translation import ugettext as _
from guardian.forms import UserObjectPermissionsForm


class PermissionsTranslationMixin(object):
    def __init__(self, *args, **kwargs):
        super(PermissionsTranslationMixin, self).__init__(*args, **kwargs)
        choices = [(key, _(value)) for key, value in self.fields['permissions'].choices]
        self.fields['permissions'].choices = choices


class TranslatedUserObjectPermissionsForm(PermissionsTranslationMixin, UserObjectPermissionsForm):
    pass
