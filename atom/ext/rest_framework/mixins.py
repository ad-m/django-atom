from django.urls import reverse_lazy as reverse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


class ViewSetTestCaseMixin(object):
    def get_user_factory_cls(self):
        if hasattr(self, 'USER_FACTORY'):
            return self.USER_FACTORY
        if hasattr(settings, 'TESTS_USER_FACTORY'):
            return import_string(settings.TESTS_USER_FACTORY)
        raise ImproperlyConfigured('{0} is missing a {0}.USER_FACTORY or settings is missing TESTS_USER_FACTORY. '
                                   'Define {0}.USER_FACTORY or settings.TESTS_USER_FACTORY or override '
                                   '{0}.get_user_factory_cls().'.format(self.__class__.__name__))

    def setUp(self, *args, **kwargs):
        super(ViewSetTestCaseMixin, self).setUp(*args, **kwargs)
        self.object = self.FACTORY_CLS()
        self.client.login(username=self.get_user_factory_cls()(), password='pass')

    def test_detail_http_status(self):
        url = reverse(self.DETAIL_VIEW, kwargs={'pk': self.object.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_http_status(self):
        url = reverse(self.LIST_VIEW)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_queries_limit(self):
        self.FACTORY_CLS.create_batch(size=20)
        url = reverse(self.DETAIL_VIEW, kwargs={'pk': self.object.pk})
        with self.assertNumQueriesLessThan(self.QUERY_LIMIT):
            self.client.get(url)

    def test_list_queries_limit(self):
        self.FACTORY_CLS.create_batch(size=20)
        url = reverse(self.LIST_VIEW)
        with self.assertNumQueriesLessThan(self.QUERY_LIMIT):
            self.client.get(url)
