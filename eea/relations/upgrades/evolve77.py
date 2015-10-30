""" Upgrades for eea.relations 7.7
"""

import logging
import transaction
from persistent.list import PersistentList
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger("eea.relations.upgrades")

def add_eea_refs(context):
    """
    Add the eea_refs attribute to objects
    if the object has related items, put them in eea_refs
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool()
    total = len(brains)
    logger.info("Total of %s objects" %total)
    count = 0
    for brain in brains:
        count += 1
        if count%100 == 0:
            logger.info('INFO: Subtransaction committed to zodb (%s/%s)',
                        count, total)
            transaction.commit()

        try:
            obj = brain.getObject()
            try:
                obj.eea_refs = PersistentList(obj.getRawRelatedItems())
            except Exception:
                obj.eea_refs = PersistentList()
        except Exception:
            logger.warn("brain with problems: %s" %brain.getPath())
    logger.info("Done adding eea_refs on objects")
