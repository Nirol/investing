from typing import List


from marshmallow import ValidationError, fields, post_load, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.extensions import db

# many to many relationship table between line item and ad unit
from app.models.ad_unit.ad_unit import AdUnit, AdUnitSchema
from app.models.base_model import BaseModel
from app.models.base_schema import BaseSchema

# import is required
from app.models.creative.creative import Creative #noqa


ad_unit_line_item = db.Table('ad_unit_line_item',
                    db.Column('line_item_id', db.Integer, db.ForeignKey('line_item.id'), primary_key=True),
                    db.Column('ad_unit_id', db.Integer, db.ForeignKey('ad_unit.id'), primary_key=True)
                    )

class LineItem(BaseModel):
    __tablename__ = 'line_item'


    max_impressions = db.Column(db.Integer)
    rpm = db.Column(db.Numeric)

    campaign_start = db.Column(db.TIMESTAMP(timezone=False))
    campaign_end = db.Column(db.TIMESTAMP(timezone=False))

    ad_units = db.relationship('AdUnit', secondary=ad_unit_line_item, backref=db.backref('line_item'))
    creatives = db.relationship('Creative', backref='LineItem', lazy=True)

    def __init__(self, **kwargs):
        super(LineItem, self).__init__(**kwargs)
        # do custom initialization here


class LineItemSchema(BaseSchema, SQLAlchemyAutoSchema):
    LINE_ITEM_UPDATABLE_FIELDS = ["max_impressions", "rpm", "campaign_start", "campaign_end", "ad_unit_ids"]

    @pre_load()
    def convert_datetime(self,data, **kwargs):
        """
        The Line Item schema expect the campaign start and end datetime object
        as strings.
        Loading existing objects for validation purposes require converting the
        datetime objects into strings.
        """
        from datetime import datetime
        def _convert_datetime_to_str(data,field_name,field_value):
            if isinstance(field_value, datetime):
                data[field_name] = str(field_value)



        campaign_start = data.get("campaign_start",None)
        _convert_datetime_to_str(data,field_name="campaign_start", field_value=campaign_start )

        campaign_end = data.get("campaign_end", None)
        _convert_datetime_to_str(data, field_name="campaign_end", field_value=campaign_end)

        return data


    @post_load()
    def add_ad_units(self, data, **kwargs):
        """
        query the ad_unit_ids param and add AdUnit objects to the data

        raise ValidationError in case an ad_unit_id received does not exist in the AdUnit table.
        """
        ad_unit_ids = data.pop("ad_unit_ids", None)
        if ad_unit_ids:
            ad_unit_ids = set(ad_unit_ids)
            data["ad_units"]: List[AdUnit] = AdUnit.query.filter(AdUnit.id.in_(ad_unit_ids)).all()
            if len(ad_unit_ids) != len(data["ad_units"]):
                # at least one of ad_unit_ids do not exist in the ad units database!
                existing_ids = [ad_unit.id for ad_unit in data["ad_units"]]
                non_existing_ids = [ad_unit_id for ad_unit_id in ad_unit_ids if ad_unit_id not in existing_ids]
                raise ValidationError(f"{non_existing_ids} ad unit ids does not exist!")


        return data


    ad_unit_ids = fields.List(fields.Integer(), load_only=True)
    ad_units = fields.List(fields.Nested(AdUnitSchema()), dump_only=True)

    class Meta:
        model = LineItem