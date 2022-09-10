import enum


#  declaring enums as a subclass of str to avoid
#  marshmallow serializing issues.
class Language(str, enum.Enum):
    ENGLISH = ("ENGLISH",)
    HEBREW = ("HEBREW",)
    JAPANESE = "JAPANESE"
