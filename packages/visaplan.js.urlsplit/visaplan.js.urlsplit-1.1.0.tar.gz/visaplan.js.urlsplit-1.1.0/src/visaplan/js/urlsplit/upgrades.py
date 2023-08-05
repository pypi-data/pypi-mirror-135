# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

from logging import getLogger

# Zope:
from Products.CMFCore.utils import getToolByName

from plone.app.upgrade.utils import loadMigrationProfile


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-visaplan.js.urlsplit:default',
    )


def load_and_cook_javascript(context, logger=None):
    tuples = [
        ('jsregistry',  'portal_javascripts'),
        ]
    setup = getToolByName(context, 'portal_setup')
    run_step = setup.runImportStepFromProfile
    if logger is None:
        logger = getLogger('visaplan.js.urlsplit')
    info = logger.info
    profile = 'profile-visaplan.js.urlsplit:default'
    for xmlname, toolname in tuples:
        info('Profile %(profile)r: %(xmlname)s[.xml]', locals())
        try:
            run_step(profile, xmlname)
        except Exception as e:
            logger.error('error running %(xmlname)r[.xml] from %(profile)s',
                         locals())
            logger.error('Exception: %(e)r', locals())
            logger.error('e.args: %s', (e.args,))
            raise

        tool = getToolByName(context, toolname)
        info('toolname %(toolname)r --> tool %(tool)r', locals())
        try:
            tool.cookResources()
        except AttributeError as e:
            logger.error('%(xmlname)s[.xml]: '
                         'The %(toolname)r tool lacks a cookResources method'
                         ' %(tool)r',
                         locals())
            raise
        else:
            info('%(xmlname)s resources cooked.', locals())
