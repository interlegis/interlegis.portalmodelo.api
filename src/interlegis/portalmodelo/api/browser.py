# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.api.controlpanel import IPortalSettings
from interlegis.portalmodelo.api.utils import type_cast
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.registry.interfaces import IRegistry
from Products.Archetypes.interfaces import IBaseContent
from Products.CMFCore.interfaces import IFolderish
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getUtility

import json

FOLDER_IDS = [
    'despesas', 'transferencias', 'receitas', 'acompanhamento', 'licitacoes']
SERIALIZABLE_FIELD_NAMES = [
    'title', 'description', 'creation_date', 'modification_date',
    'start_date', 'end_date', 'remoteUrl', 'file', 'image']


class PortalJSONView(grok.View):
    """Generates a JSON with information about the portal.
    """
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('portalmodelo-json')

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')

        j = {}
        # walk over all fields of the configlet Schema
        for r in self.fields:
            j[r] = type_cast(getattr(self.settings, r))

        return json.dumps(j, sort_keys=True, indent=4)

    def update(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IPortalSettings)
        self.fields = IPortalSettings.names()


class TransparencyJSONView(grok.View):
    """Generates a JSON with content of a folder called "Transparência".
    """
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('transparency-json')

    def update(self):
        self.folder = getattr(api.portal.get(), 'transparencia', None)
        self.catalog = api.portal.get_tool('portal_catalog')

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        j = {}
        if self.folder and IFolderish.providedBy(self.folder):
            for id in FOLDER_IDS:
                if hasattr(self.folder, id):
                    j[id] = self.get_folder_contents(id)
        return json.dumps(j, sort_keys=True, indent=4)

    def serialize(self, results):
        """Serialize fields of a list of content type objects.

        :param results: [required] list of objects to be serialized
        :type results: list of catalog brains
        :returns: list of serialized objects
        :rtype: list of dictionaries
        """
        s = []
        for obj in results:
            # initialize a dictionary with the object uri
            # XXX: should we use the UUID?
            fields = dict(uri=obj.absolute_url())
            # continue with the rest of the fields
            if IBaseContent.providedBy(obj):
                obj_fields = obj.Schema().fields()
                obj_fields = [(f.getName(), f.get(obj)) for f in obj_fields]
            else:
                schema = getUtility(IDexterityFTI, name=obj.portal_type).lookupSchema()
                obj_fields = [(f, getattr(obj, f)) for f in schema]
            for name, data in obj_fields:
                if name in SERIALIZABLE_FIELD_NAMES:
                    fields[name] = type_cast(data, name, obj)
            s.append(fields)
        return s

    def get_folder_contents(self, id):
        """Return list of content objects inside the object which id as a list
        of dictionaries.
        """
        if IFolderish.providedBy(self.folder[id]):
            results = self.folder[id].listFolderContents()
        else:
            results = []
        return self.serialize(results)
