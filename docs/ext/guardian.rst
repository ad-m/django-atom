Django-guardian
===============

There is some extensions for `django-guardian <https://github.com/django-guardian/django-guardian>`_ package. 

Forms
+++++

.. automodule:: atom.ext.guardian.forms
    :members:
    :undoc-members:

Tests
+++++

Example usage
-------------

.. code:: python

    from django.core.urlresolvers import reverse
    from django.test import TestCase

    from atom.ext.guardian.tests import PermissionStatusMixin
    from feder.monitorings.factories import MonitoringFactory
    from feder.users.factories import UserFactory

    class ObjectMixin(object):
        def setUp(self):
            self.user = UserFactory(username='john')
            self.monitoring = self.permission_object = MonitoringFactory()
            self.case = CaseFactory(monitoring=self.monitoring)
            self.from_user = OutgoingLetterFactory(title='Wniosek',
                                                   case__monitoring=self.monitoring)
            self.from_institution = IncomingLetterFactory(title='Odpowiedz',
                                                          case__monitoring=self.monitoring)

    class LetterRssFeedTestCase(ObjectMixin, PermissionStatusMixin, TestCase):
        status_anonymous = 200
        status_no_permission = 200
        permission = []

        def get_url(self):
            return reverse('letters:rss')

Docstrings
-------------

.. automodule:: atom.ext.guardian.tests
    :members:
    :undoc-members:


