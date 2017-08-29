from django.test.runner import DiscoverRunner


class TestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        return super(TestRunner, self).setup_databases(**kwargs)
