""" Field interfaces
"""
from zope.interface import Interface

try:
    from eea.workflow import interfaces
    IValueProvider = interfaces.IValueProvider
    IRequiredFor = interfaces.IRequiredFor
except ImportError:
    # eea.workflow is not mandatory
    class IValueProvider(Interface):
        """ Value provider """
        pass

    class IRequiredFor(Interface):
        """ Required for """
        pass
