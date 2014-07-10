# -*- coding: utf-8 -*-
from interlegis.portalmodelo.api import _
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

PROJECTNAME = 'interlegis.portalmodelo.api'

REGISTER_URL = 'http://www.interlegis.leg.br/registrar?produto=portalmodelo&amp;versao=3.0'


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'interlegis.portalmodelo.api:uninstall',
            u'interlegis.portalmodelo.api.upgrades.v1010:default'
        ]

KINDS = SimpleVocabulary([
    SimpleTerm(value=u'assembleia-legislativa', title=_(u'Assembleia Legislativa')),
    SimpleTerm(value=u'camara-dos-deputados', title=_(u'Câmara dos Deputados')),
    SimpleTerm(value=u'camara-legislativa', title=_(u'Câmara Legislativa')),
    SimpleTerm(value=u'camara-municipal', title=_(u'Câmara Municipal')),
    SimpleTerm(value=u'outro', title=_(u'Outro')),
    SimpleTerm(value=u'senado-federal', title=_(u'Senado Federal')),
    SimpleTerm(value=u'tribunal-de-contas-da-uniao', title=_(u'Tribunal de Contas da União')),
    SimpleTerm(value=u'tribunal-de-contas-estadual', title=_(u'Tribunal de Contas Estadual')),
    SimpleTerm(value=u'tribunal-de-contas-municipal', title=_(u'Tribunal de Contas Municipal')),
])
