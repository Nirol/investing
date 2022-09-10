from sqlalchemy import UniqueConstraint
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.ad_unit.enums import Device,Browser, Language, OperatingSystem
from app.extensions import db
from app.models.base_model import BaseModel
from app.models.base_schema import BaseSchema


class AdUnit(BaseModel):
    __tablename__ = 'ad_unit'

    # the five fields defining a unique ad unit:

    # simplified the implementation using string type for country ( only in assignment)
    country = db.Column(db.String(80), nullable=False)
    device = db.Column(db.Enum(Device), nullable=False)
    browser = db.Column(db.Enum(Browser), nullable=False)
    language = db.Column(db.Enum(Language), nullable=False)
    os = db.Column(db.Enum(OperatingSystem), nullable=False)

    # add the unique constraint
    __table_args__ = (UniqueConstraint('country', 'device','browser','language','os',name='_ad_unit_uc'),
                      )

    def __init__(self, **kwargs):
        # do custom initialization here
        super(AdUnit, self).__init__( **kwargs)


class AdUnitSchema(BaseSchema, SQLAlchemyAutoSchema ):
    AD_UNIT_UPDATABLE_FIELDS = ["country", "device", "browser", "language", "os"]

    class Meta:
        model = AdUnit