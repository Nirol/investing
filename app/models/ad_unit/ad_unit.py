from datetime import datetime
from typing import Dict

from sqlalchemy import UniqueConstraint
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.ad_unit.enums import Device,Browser, Language, OperatingSystem
from app.extensions import db


class AdUnit(db.Model):
    __tablename__ = 'ad_unit'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)

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

    def updatable_fields_json(self)->Dict:
        """
        return python dict with only the updatable object fields.
        """
        obj_dict = self.__dict__
        updatable_fields = {}
        for field in AdUnitSchema.UPDATABLE_FIELDS:
            updatable_fields[field] = obj_dict[field]

        return updatable_fields

    def __init__(self, **kwargs):
        super(AdUnit, self).__init__(**kwargs)
        # do custom initialization here


class AdUnitSchema(SQLAlchemyAutoSchema):
    UPDATABLE_FIELDS = ["country", "device", "browser", "language", "os"]


    @staticmethod
    def is_patch_fields_valid(data:Dict) ->bool:
        """

        :param data: the request payload body.
        :return: if the requestt payload contain only updatable AdUnit fields.
        """
        for key in data.keys():
            if key  not in AdUnitSchema.UPDATABLE_FIELDS:
                return False

        return True


    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    id = fields.Integer(dump_only=True)

    class Meta:
        model = AdUnit