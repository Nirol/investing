from datetime import datetime

from app.extensions import db
from app.models.creative.enums import CreativeType


class Creative(db.Model):
    __tablename__ = 'creative'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)

    creative_type = db.Column(db.Enum(CreativeType), nullable=False)
    # either url link or html code text.
    content = db.Column(db.Text, nullable=False)

    width = db.Column(db.Numeric(6, 2))
    height = db.Column(db.Numeric(6, 2))

    line_item_id = db.Column(db.Integer, db.ForeignKey('line_item.id'),
        nullable=False)

