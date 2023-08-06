# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from iaweb.privacy.testing import IAWEB_PRIVACY_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that iaweb.privacy is properly installed."""

    layer = IAWEB_PRIVACY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if iaweb.privacy is installed."""
        self.assertTrue(self.installer.isProductInstalled("iaweb.privacy"))

    def test_browserlayer(self):
        """Test that IIawebPrivacyLayer is registered."""
        from iaweb.privacy.interfaces import IIawebPrivacyLayer
        from plone.browserlayer import utils

        self.assertIn(IIawebPrivacyLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IAWEB_PRIVACY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["iaweb.privacy"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if iaweb.privacy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("iaweb.privacy"))

    def test_browserlayer_removed(self):
        """Test that IIawebPrivacyLayer is removed."""
        from iaweb.privacy.interfaces import IIawebPrivacyLayer
        from plone.browserlayer import utils

        self.assertNotIn(IIawebPrivacyLayer, utils.registered_layers())
