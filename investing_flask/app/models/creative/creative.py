from typing import Union

from marshmallow import post_load, ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.extensions import db
from app.models.base_model import BaseModel
from app.models.base_schema import BaseSchema
from app.models.creative.enums import CreativeType


class Creative(BaseModel):
    __tablename__ = "creative"

    creative_type = db.Column(db.Enum(CreativeType), nullable=False)
    # either url link or html code text.
    content = db.Column(db.Text, nullable=False)

    width = db.Column(db.Numeric(6, 2))
    height = db.Column(db.Numeric(6, 2))

    line_item_id = db.Column(db.Integer, db.ForeignKey("line_item.id"), nullable=False)

    def __init__(self, **kwargs):
        # do custom initialization here
        super(Creative, self).__init__(**kwargs)


class CreativeSchema(BaseSchema, SQLAlchemyAutoSchema):

    CREATIVE_UPDATABLE_FIELDS = ["creative_type", "content", "width", "height", "campaign_end", "line_item_id"]

    @post_load()
    def add_line_item(self, data, **kwargs):
        """
        query the ad_unit_ids param and add AdUnit objects to the data

        raise ValidationError in case an ad_unit_id received does not exist in the AdUnit table.
        """

        line_item_id = data.pop("line_item_id", None)
        if line_item_id:
            from app.models.line_item.line_item import LineItem

            line_item: Union[LineItem, None] = LineItem.query.get(line_item_id)
            if not line_item:
                raise ValidationError(f"{line_item} line item id does not exist!")

            data["line_item_id"] = line_item.id
        return data

    line_item_id = fields.Integer()

    class Meta:
        model = Creative
