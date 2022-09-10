import enum


#  declaring enums as a subclass of str to avoid
#  marshmallow serializing issues.
class Browser(str, enum.Enum):
    SAFARI = ("SAFARI",)
    CHROME = ("CHROME",)
    FIREFOX = ("FIREFOX",)
    NETSCAPE = ("NETSCAPE",)
