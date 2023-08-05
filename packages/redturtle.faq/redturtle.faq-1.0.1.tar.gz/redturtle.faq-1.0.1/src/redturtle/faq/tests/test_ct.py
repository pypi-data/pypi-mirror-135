# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from redturtle.faq.testing import REDTURTLE_FAQ_INTEGRATION_TESTING

import unittest


class TestContentTypes(unittest.TestCase):
    """"""

    layer = REDTURTLE_FAQ_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_faq_folder_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("FaqFolder", "Faq", "Image", "File"),
            portal_types["FaqFolder"].allowed_content_types,
        )

    def test_faq_addable_types(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            ("Image", "File"),
            portal_types["Faq"].allowed_content_types,
        )
