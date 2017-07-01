from django.core.exceptions import ImproperlyConfigured

try:
    from django.urls import reverse  # Django 1.10+
except ImportError:  # Django 1.9
    from django.core.urlresolvers import reverse


class AdminTestCaseMixin(object):
    user_factory_cls = None
    factory_cls = None
    model = None
    changelist_viewname = None
    change_viewname = None
    delete_viewname = None
    history_viewname = None
    QUERY_LIMIT = 30

    def get_changelist_viewname(self):
        if self.changelist_viewname is None and self.model is None:
            raise ImproperlyConfigured('{0} is missing a {0}.changelist_viewname or {0}.model. Define '
                                       '{0}.changelist_viewname or {0}.model or override '
                                       '{0}.get_changelist_viewname().'.format(self.__class__.__name__))
        return self.changelist_viewname or 'admin:{}_{}_changelist'.format(self.model._meta.app_label,
                                                                           self.model._meta.model_name)

    def get_change_viewname(self):
        if self.change_viewname is None and self.model is None:
            raise ImproperlyConfigured('{0} is missing a {0}.change_viewname or {0}.model. Define '
                                       '{0}.change_viewname or {0}.model or override '
                                       '{0}.get_change_viewname().'.format(self.__class__.__name__))
        return self.changelist_viewname or 'admin:{}_{}_change'.format(self.model._meta.app_label,
                                                                       self.model._meta.model_name)

    def get_delete_viewname(self):
        if self.delete_viewname is None and self.model is None:
            raise ImproperlyConfigured('{0} is missing a {0}.changelist_viewname or {0}.model. Define '
                                       '{0}.change_viewname or {0}.model or override '
                                       '{0}.get_delete_viewname().'.format(self.__class__.__name__))
        return self.delete_viewname or 'admin:{}_{}_delete'.format(self.model._meta.app_label,
                                                                   self.model._meta.model_name)

    def get_history_viewname(self):
        if self.history_viewname is None and self.model is None:
            raise ImproperlyConfigured('{0} is missing a {0}.history_viewname or {0}.model. Define '
                                       '{0}.history_viewname or {0}.model or override '
                                       '{0}.get_history_viewname().'.format(self.__class__.__name__))
        return self.history_viewname or 'admin:{}_{}_history'.format(self.model._meta.app_label,
                                                                     self.model._meta.model_name)

    def get_factory_cls(self):
        if self.factory_cls is None:
            raise ImproperlyConfigured('{0} is missing a {0}.factory_cls. Define {0}.factory_cls or override '
                                       '{0}.get_factory_cls().'.format(self.__class__.__name__))
        return self.factory_cls

    def setUp(self):
        if not hasattr(self, 'assertNumQueriesLessThan'):
            self.skipTest("{0} is missing a {0}.assertNumQueriesLessThan method. "
                          "Use test_plus.test.TestCase as base class.".format(self.__class__.__name__))
        self.object = self.factory_cls()
        self.user = self.user_factory_cls(password='password',
                                          is_superuser=True,
                                          is_staff=True)
        self.client.login(username=self.user.username, password='password')

    def test_status_changelist(self):
        url = reverse(self.get_changelist_viewname())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Invalid status code on '{}'".format(url))

    def test_status_change_view(self):
        url = reverse(self.get_change_viewname(), args=[self.object.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Invalid status code on '{}'".format(url))

    def test_status_delete_view(self):
        url = reverse(self.get_delete_viewname(), args=[self.object.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Invalid status code on '{}'".format(url))

    def test_status_history_view(self):
        url = reverse(self.get_history_viewname(), args=[self.object.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, "Invalid status code on '{}'".format(url))

    def test_changelist_queries_limit(self):
        self.factory_cls.create_batch(size=20)
        url = reverse(self.get_changelist_viewname())
        with self.assertNumQueriesLessThan(self.QUERY_LIMIT):
            self.client.get(url)

    def test_change_view_queries_limit(self):
        self.factory_cls.create_batch(size=20)
        url = reverse(self.get_change_viewname(), args=[self.object.pk])
        with self.assertNumQueriesLessThan(self.QUERY_LIMIT):
            self.client.get(url)
