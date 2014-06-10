# -*- coding: utf-8 -*-

from interlegis.portalmodelo.api.config import PROJECTNAME
from interlegis.portalmodelo.api.controlpanel import IPortalSettings
from interlegis.portalmodelo.api.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view('portalmodelo-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@portalmodelo-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('portalmodelo', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('portalmodelo', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IPortalSettings)

    def test_title_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'title'))
        self.assertIsNone(self.settings.title)

    def test_kind_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'kind'))
        self.assertIsNone(self.settings.kind)

    def test_address_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'address'))
        self.assertIsNone(self.settings.address)

    def test_postal_code_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'postal_code'))
        self.assertIsNone(self.settings.postal_code)

    def test_city_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'city'))
        self.assertIsNone(self.settings.city)

    def test_state_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'state'))
        self.assertIsNone(self.settings.state)

    def test_id_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'id'))
        self.assertIsNone(self.settings.id)

    def test_telephone_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'telephone'))
        self.assertIsNone(self.settings.telephone)

    def test_email_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'email'))
        self.assertIsNone(self.settings.email)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        BASE_REGISTRY = 'interlegis.portalmodelo.api.controlpanel.IPortalSettings.'
        records = [
            BASE_REGISTRY + 'title',
            BASE_REGISTRY + 'kind',
            BASE_REGISTRY + 'address',
            BASE_REGISTRY + 'postal_code',
            BASE_REGISTRY + 'city',
            BASE_REGISTRY + 'state',
            BASE_REGISTRY + 'id',
            BASE_REGISTRY + 'telephone',
            BASE_REGISTRY + 'email',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
