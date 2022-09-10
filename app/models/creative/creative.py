from app.extensions import db
from app.models.base_model import BaseModel
from app.models.creative.enums import CreativeType


class Creative(BaseModel):
    __tablename__ = 'creative'

    creative_type = db.Column(db.Enum(CreativeType), nullable=False)
    # either url link or html code text.
    content = db.Column(db.Text, nullable=False)

    width = db.Column(db.Numeric(6, 2))
    height = db.Column(db.Numeric(6, 2))

    line_item_id = db.Column(db.Integer, db.ForeignKey('line_item.id'),
        nullable=False)

    def __init__(self, **kwargs):
        # do custom initialization here
        super(Creative, self).__init__( **kwargs)
