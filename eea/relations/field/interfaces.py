from zope.interface import Interface

# eea.workflow is not mandatory
try:
    from eea.workflow.interfaces import IValueProvider
    IValueProvider #pyflakes
except ImportError:
    class IValueProvider(Interface): pass

try:
    from eea.workflow.interfaces import IRequiredFor
    IRequiredFor #pyflakes
except ImportError:
    class IRequiredFor(Interface): pass
