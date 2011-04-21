from Products.Archetypes.Registry import registerField
from referencefield import EEAReferenceField

def register():
    registerField(
        EEAReferenceField,
        title="EEA Reference Field",
        description=("EEA Reference field that knows about is_required_for.")
    )
