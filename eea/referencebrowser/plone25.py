#
# Plone 2.5 Backward compatible
#
try:
    from Products.CMFPlone.CatalogTool import _eioRegistry
    def object_provides(object, portal, **kw):
        return [i.__identifier__ for i in providedBy(object).flattened()]

    if not _eioRegistry.has_key('object_provides'):
        _eioRegistry.register('object_provides', object_provides)
except ImportError, err:
    pass
#
# Plone 2.5 register skins directory
#
try:
    import zope.annotation
except ImportError:
    #BBB Plone 2.5
    from os.path import dirname
    from Globals import package_home
    from Products.CMFCore import utils as cmfutils
    from Products.CMFCore.DirectoryView import registerDirectory

    ppath = cmfutils.ProductsPath
    cmfutils.ProductsPath.append(dirname(package_home(globals())))
    registerDirectory('skins', globals())
    cmfutils.ProductsPath = ppath
