import enum

#  declaring enums as a subclass of str to avoid
#  marshmallow serializing issues.
class Device(str, enum.Enum):
    MOBILE = 'MOBILE',
    DESKTOP = 'DESKTOP'
