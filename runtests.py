import os
import sys

try:
    import django
    from django.test.utils import get_runner
    os.environ['DJANGO_SETTINGS_MODULE'] = 'testapp.settings'
    django.setup()

    import atom.ext.autocomplete_light.filters
    import atom.ext.guardian.tests
    from django.conf import settings
except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
