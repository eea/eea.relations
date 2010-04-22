""" Doc tests
"""
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from base import EEARelationsFunctionalTestCase

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    return unittest.TestSuite((
            Suite('docs/graph.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.relations',
                  test_class=EEARelationsFunctionalTestCase) ,
            Suite('docs/components.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.relations',
                  test_class=EEARelationsFunctionalTestCase) ,
            Suite('docs/faceted.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.relations',
                  test_class=EEARelationsFunctionalTestCase) ,
    ))
