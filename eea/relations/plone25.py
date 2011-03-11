#
# Plone 2.5 Backward compatible
#
import logging
logger = logging.getLogger("eea.relations.plone25")

try:
    from Products.CMFPlone.CatalogTool import _eioRegistry
    from zope.interface import providedBy
    def object_provides(obj, portal, **kw):
        return [i.__identifier__ for i in providedBy(obj).flattened()]

    if not _eioRegistry.has_key('object_provides'):
        _eioRegistry.register('object_provides', object_provides)
except ImportError, err:
    logger.info(err)
#
# Plone 2.5 register skins directory
#
try:
    import zope.annotation
    zope.annotation #pyflakes
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
