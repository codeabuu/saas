from django.test import TestCase
from django.conf import settings
import os
from decouple import config

# Create your tests here.

os.environ["DATABASE_URL"] = config("DATABASE_URL")
class NeonDBTestCase(TestCase):
    def test_db_url(self):
        DATABASE_URL=settings.DATABASE_URL
        self.assertIn("neon.tech", DATABASE_URL)