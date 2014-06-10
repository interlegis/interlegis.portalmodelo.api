# -*- coding: utf-8 -*-

from interlegis.portalmodelo.api.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    """Atualiza perfil para versao 1010."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-interlegis.portalmodelo.api.upgrades.v1010:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 1010')
