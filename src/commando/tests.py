from django.test import TestCase
from django.conf import settings
import os
from decouple import config

# Create your tests here.

class NeonDBTestCase(TestCase):
    def test_db_url(self):
        DATABASE_URL=os.environ.get("DATABASE_URL")
        self.assertIn("neon.tech", DATABASE_URL)