# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2
from plone.restapi.testing import PloneRestApiDXLayer
import redturtle.faq
import plone.restapi


class RedturtleFaqLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.faq)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "redturtle.faq:default")


REDTURTLE_FAQ_FIXTURE = RedturtleFaqLayer()


REDTURTLE_FAQ_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_FAQ_FIXTURE,),
    name="RedturtleFaqLayer:IntegrationTesting",
)


REDTURTLE_FAQ_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_FAQ_FIXTURE,), name="RedturtleFaqLayer:FunctionalTesting",
)


class RedturtleFaqRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.faq)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "redturtle.faq:default")


REDTURTLE_FAQ_API_FIXTURE = RedturtleFaqRestApiLayer()
REDTURTLE_FAQ_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_FAQ_API_FIXTURE,),
    name="RedturtleFaqRestApiLayer:Integration",
)

REDTURTLE_FAQ_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_FAQ_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="RedturtleFaqRestApiLayer:Functional",
)
