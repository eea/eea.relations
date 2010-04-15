""" Widget
"""
from Products.Archetypes.Widget import ReferenceWidget

class EEAReferenceBrowserWidget(ReferenceWidget):
    """ Custom Reference Browser Widget
    """
    _properties = ReferenceWidget._properties.copy()
    _properties.update({
        'macro' : "eeareferencebrowser",
        'helper_js': ('eeareferencebrowser.js',),
        'helper_css': ('eeareferencebrowser.css',)
    })
