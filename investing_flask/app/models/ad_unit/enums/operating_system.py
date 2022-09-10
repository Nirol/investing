import enum


#  declaring enums as a subclass of str to avoid
#  marshmallow serializing issues.
class OperatingSystem(str, enum.Enum):
    IOS = ("IOS",)
    ANDROID = "ANDROID"
    WINDOWS = "WINDOWS"
