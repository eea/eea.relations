""" Base test cases
"""
from Products.Five import zcml
from Products.Five import fiveconfigure

product_globals = globals()

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_eea_widget_referencebrowser():
    """Set up the additional products.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import Products.Five
    zcml.load_config('meta.zcml', Products.Five)

    import eea.widget.referencebrowser
    zcml.load_config('configure.zcml', eea.widget.referencebrowser)
    fiveconfigure.debug_mode = False

    ptc.installProduct('Five')

    # Plone 2.x compatible
    try: import Products.FiveSite
    except ImportError: pass
    else: ptc.installProduct('FiveSite')

setup_eea_widget_referencebrowser()
ptc.setupPloneSite(extension_profiles=('eea.widget.referencebrowser:a',))

class ReferenceBrowserWidgetTestCase(ptc.PloneTestCase):
    """Base class for integration tests for the 'EEA ReferenceBrowser Widget' product.
    """

class ReferenceBrowserWidgetFunctionalTestCase(ptc.FunctionalTestCase, ReferenceBrowserWidgetTestCase):
    """Base class for functional integration tests for the 'EEA ReferenceBrowser Widget' product.
    """
