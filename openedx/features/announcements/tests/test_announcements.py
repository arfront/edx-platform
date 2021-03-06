"""
Unit tests for the announcements feature.
"""

from __future__ import absolute_import

import json
import unittest
from mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from student.tests.factories import AdminFactory

from openedx.features.announcements.models import Announcement

TEST_ANNOUNCEMENTS = [
    ("Active Announcement", True),
    ("Inactive Announcement", False),
    ("Another Test Announcement", True),
    ("<strong>Formatted Announcement</strong>", True),
    ("<a>Other Formatted Announcement</a>", True),
]


@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class TestGlobalAnnouncements(TestCase):
    """
    Test Announcements in LMS
    """

    @classmethod
    def setUpTestData(cls):
        super(TestGlobalAnnouncements, cls).setUpTestData()
        Announcement.objects.bulk_create([
            Announcement(content=content, active=active)
            for content, active in TEST_ANNOUNCEMENTS
        ])

    def setUp(self):
        super(TestGlobalAnnouncements, self).setUp()
        self.client = Client()
        self.admin = AdminFactory.create(
            email='staff@edx.org',
            username='admin',
            password='pass'
        )
        self.client.login(username=self.admin.username, password='pass')

    @patch.dict(settings.FEATURES, {'ENABLE_ANNOUNCEMENTS': False})
    def test_feature_flag_disabled(self):
        """Ensures that the default settings effectively disables the feature"""
        response = self.client.get('/dashboard')
        self.assertNotIn('AnnouncementsView', response.content)
        self.assertNotIn('<div id="announcements"', response.content)

    def test_feature_flag_enabled(self):
        """Ensures that enabling the flag, enables the feature"""
        response = self.client.get('/dashboard')
        self.assertIn('AnnouncementsView', response.content)

    def test_pagination(self):
        url = reverse("announcements:page", kwargs={"page": 1})
        response = self.client.get(url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(data['num_pages'], 1)
        ## double the number of announcements to verify the number of pages increases
        self.setUpTestData()
        response = self.client.get(url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEquals(data['num_pages'], 2)

    def test_active(self):
        """
        Ensures that active announcements are visible on the dashboard
        """
        url = reverse("announcements:page", kwargs={"page": 1})
        response = self.client.get(url)
        self.assertIn("Active Announcement", response.content)

    def test_inactive(self):
        """
        Ensures that inactive announcements aren't visible on the dashboard
        """
        url = reverse("announcements:page", kwargs={"page": 1})
        response = self.client.get(url)
        self.assertNotIn("Inactive Announcement", response.content)

    def test_formatted(self):
        """
        Ensures that formatting in announcements is rendered properly
        """
        url = reverse("announcements:page", kwargs={"page": 1})
        response = self.client.get(url)
        self.assertIn("<strong>Formatted Announcement</strong>", response.content)
