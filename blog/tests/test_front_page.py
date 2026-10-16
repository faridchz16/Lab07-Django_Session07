from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from django.test.utils import CaptureQueriesContext
from django.db import connection


class FrontPageTestCase(TestCase):

    def setUp(self):
        call_command('seed_blog', verbosity=0)

    def test_front_page_runs_two_queries(self):
        url = reverse('front_page')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        query_count = len(queries)
        self.assertLessEqual(
            query_count, 2,
            f"Front page ran {query_count} queries instead of 2. Captured queries:\n" +
            "\n".join([q['sql'] for q in queries])
        )
