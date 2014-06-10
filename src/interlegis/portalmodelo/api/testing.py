# -*- coding: utf-8 -*-

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import interlegis.portalmodelo.api
        self.loadZCML(package=interlegis.portalmodelo.api)

    def setUpPloneSite(self, portal):
        self.applyProfile(
            portal, 'interlegis.portalmodelo.api:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='interlegis.portalmodelo.api:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='interlegis.portalmodelo.api:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='interlegis.portalmodelo.api:Robot',
)
