# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import iaweb.privacy


class IawebPrivacyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=iaweb.privacy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "iaweb.privacy:default")


IAWEB_PRIVACY_FIXTURE = IawebPrivacyLayer()


IAWEB_PRIVACY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IAWEB_PRIVACY_FIXTURE,), name="IawebPrivacyLayer:IntegrationTesting"
)


IAWEB_PRIVACY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IAWEB_PRIVACY_FIXTURE,), name="IawebPrivacyLayer:FunctionalTesting"
)


IAWEB_PRIVACY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(IAWEB_PRIVACY_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="IawebPrivacyLayer:AcceptanceTesting",
)
