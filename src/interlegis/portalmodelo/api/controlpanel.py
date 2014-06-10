# -*- coding: utf-8 -*-
"""Define the control panel configlet; the title field must be synchronized
with the portal title property.
"""
from interlegis.portalmodelo.api import _
from interlegis.portalmodelo.api.config import KINDS
from interlegis.portalmodelo.api.config import REGISTER_URL
from plone import api
from plone.app.registry.browser import controlpanel
from plone.directives import form
from urlparse import urlparse
from zope import schema
from zope.globalrequest import getRequest
from zope.interface import invariant

import urllib2


class IPortalSettings(form.Schema):
    """Configlet schema.
    """

    title = schema.TextLine(
        title=_(u'Organization Name'),
        description=_(u'help_name', default=u''),
        required=True,
    )

    kind = schema.Choice(
        title=_(u'Organization Type'),
        description=_(u'help_kind', default=u''),
        vocabulary=KINDS,
        required=True,
    )

    address = schema.TextLine(
        title=_(u'Address'),
        description=_(u'help_address', default=u''),
        required=True,
    )

    postal_code = schema.ASCIILine(
        title=_(u'Postal code'),
        description=_(u'help_postal_code', default=u''),
        required=True,
    )

    city = schema.TextLine(
        title=_(u'City'),
        description=_(u'help_city', default=u''),
        required=True,
    )

    state = schema.Choice(
        title=_(u'State'),
        description=_(u'help_state', default=u''),
        required=True,
        vocabulary=u'brasil.estados',
    )

    id = schema.ASCIILine(
        title=_(u'Organization ID'),
        description=_(u'help_id', default=u''),
        required=True,
    )

    telephone = schema.ASCIILine(
        title=_(u'Telephone'),
        description=_(u'help_telephone', default=u''),
        required=True,
    )

    email = schema.ASCIILine(
        title=_(u'Email'),
        description=_(u'help_email', default=u''),
        required=True,
    )

    register = schema.Bool(
        title=_(u'Register with Interlegis?'),
        description=_(u'help_register', default=u''),
        default=True,
        required=False,
    )

    @invariant
    def update_portal_title_hook(data):
        """Set the portal title property with the value of the title field.
        This method is a hook to synchronize them when the form is saved.
        """
        portal = api.portal.get()
        portal.title = data.title

    @invariant
    def register_portal(data):
        """"Register the portal with Interlegis."""
        if data.register:
            portal_url = api.portal.get().absolute_url()
            hostname = urlparse(portal_url).hostname
            if hostname != 'localhost':  # we only register real portals
                request = urllib2.Request(REGISTER_URL)
                request.add_header('Referer', portal_url)
                result = urllib2.urlopen(request, timeout=5)
                code = result.getcode()
                if 200 <= code < 400:  # 2xx and 3xx should be considered successfull
                    type = 'info'
                    message = _(u'Site successfully registered with Interlegis!')
                else:
                    type = 'warn'
                    message = _(
                        u'An error occurred while registering the site (error code ${code})',
                        mapping={'code': code}
                    )

                request = getRequest()
                api.portal.show_message(message, request=request, type=type)


class PortalSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IPortalSettings
    label = _(u'Portal Modelo')
    description = _(u'Settings for the Portal Modelo.')

    def updateWidgets(self):
        """Set the title field with the value of the portal title property.
        This method is a hook to synchronize them when the form is loaded.
        """
        super(PortalSettingsEditForm, self).updateWidgets()
        portal = api.portal.get()
        self.widgets['title'].value = portal.title


class PortalSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PortalSettingsEditForm
