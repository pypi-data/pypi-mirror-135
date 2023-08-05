# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from redturtle.faq.testing import REDTURTLE_FAQ_INTEGRATION_TESTING

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that redturtle.faq is properly installed."""

    layer = REDTURTLE_FAQ_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if redturtle.faq is installed."""
        self.assertTrue(self.installer.is_product_installed("redturtle.faq"))

    def test_browserlayer(self):
        """Test that IRedturtleFaqLayer is registered."""
        from redturtle.faq.interfaces import IRedturtleFaqLayer
        from plone.browserlayer import utils

        self.assertIn(IRedturtleFaqLayer, utils.registered_layers())
