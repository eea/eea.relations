""" Base test cases
"""
from Products.Five import zcml
from Products.Five import fiveconfigure

product_globals = globals()

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_eea_relations():
    """Set up the additional products.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import Products.Five
    zcml.load_config('meta.zcml', Products.Five)

    import eea.relations
    zcml.load_config('configure.zcml', eea.relations)
    fiveconfigure.debug_mode = False

    try:
        ptc.installPackage('eea.relations')
    except AttributeError:
        #BBB Plone 2.5
        pass

    ptc.installProduct('Five')

    #BBB Plone 2.5
    try: 
        import Products.FiveSite
        Products.FiveSite
    except ImportError: pass
    else: ptc.installProduct('FiveSite')

setup_eea_relations()
ptc.setupPloneSite(extension_profiles=('eea.relations:a', 'eea.relations:c'))

class EEARelationsTestCase(ptc.PloneTestCase):
    """Base class for integration tests for the 'EEA Relations' product.
    """

class EEARelationsFunctionalTestCase(ptc.FunctionalTestCase, EEARelationsTestCase):
    """Base class for functional integration tests for the 'EEA Relations' product.
    """
