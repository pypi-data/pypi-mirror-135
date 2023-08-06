# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    PLONE_FIXTURE,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2

import dsgov.migration


class DsgovMigrationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=dsgov.migration)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'dsgov.migration:default')


DSGOV_MIGRATION_FIXTURE = DsgovMigrationLayer()


DSGOV_MIGRATION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DSGOV_MIGRATION_FIXTURE,),
    name='DsgovMigrationLayer:IntegrationTesting',
)


DSGOV_MIGRATION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DSGOV_MIGRATION_FIXTURE,),
    name='DsgovMigrationLayer:FunctionalTesting',
)


DSGOV_MIGRATION_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DSGOV_MIGRATION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='DsgovMigrationLayer:AcceptanceTesting',
)
