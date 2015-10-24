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
