from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.views.generic.detail import (BaseDetailView,
                                         SingleObjectTemplateResponseMixin)


class FormInitialMixin(object):

    def get_initial(self, *args, **kwargs):
        initial = super(FormInitialMixin, self).get_initial(*args, **kwargs)
        initial.update(self.request.GET.dict())
        return initial


class MessageMixin(object):
    success_message = None

    def get_success_message(self):
        if self.success_message is None:
            raise NotImplementedError("Provide success_message or get_success_message")
        return self.success_message.format(**self.object.__dict__)


class DeleteMessageMixin(object):
    hide_field = None

    def get_success_message(self):
        template = dict(object=self.object, verbose_name=self.model._meta.verbose_name)
        return _("{verbose_name} {object} deleted!").format(**template)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.hide_field:
            setattr(self.object, self.hide_field, False)
            self.object.save()
        else:
            self.object.delete()
        messages.add_message(request, messages.SUCCESS, self.get_success_message())
        return HttpResponseRedirect(success_url)


class ActionMixin(object):
    success_url = None

    def action(self):
        raise ImproperlyConfigured("No action to do. Provide a action body.")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.action()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        if self.success_url:
            self.success_url = force_text(self.success_url)
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseActionView(ActionMixin, BaseDetailView):
    """
    Base view for action on an object.
    Using this base class requires subclassing to provide a response mixin.
    """


class ActionView(SingleObjectTemplateResponseMixin, BaseActionView):
    template_name_suffix = '_action'


class ActionMessageMixin(MessageMixin):

    def post(self, request, *args, **kwargs):
        response = super(ActionMessageMixin, self).post(request, *args, **kwargs)
        messages.add_message(request, messages.SUCCESS, self.get_success_message())
        return response


class CreateMessageMixin(object):

    def get_form_valid_message(self):
        template = dict(object=self.object, verbose_name=self.model._meta.verbose_name)
        return _("{verbose_name} {object} created!").format(**template)


class UpdateMessageMixin(object):

    def get_form_valid_message(self):
        template = dict(object=self.object, verbose_name=self.model._meta.verbose_name)
        return _("{verbose_name} {object} updated!").format(**template)
