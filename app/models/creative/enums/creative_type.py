import enum

#  declaring enums as a subclass of str to avoid
#  marshmallow serializing issues.
class CreativeType(str, enum.Enum):
    IMAGE = 'IMAGE',
    HTML5 = 'HTML5',
    NATIVE = 'NATIVE',
