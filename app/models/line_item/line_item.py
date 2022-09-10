from datetime import datetime


from app.extensions import db

# many to many relationship table between line item and ad unit
ad_unit_line_item = db.Table('ad_unit_line_item',
                    db.Column('line_item_id', db.Integer, db.ForeignKey('line_item.id'), primary_key=True),
                    db.Column('ad_unit_id', db.Integer, db.ForeignKey('ad_unit.id'), primary_key=True)
                    )

class LineItem(db.Model):
    __tablename__ = 'line_item'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)


    max_impressions = db.Column(db.Integer)
    rpm = db.Column(db.Numeric)

    campaign_start = db.Column(db.TIMESTAMP(timezone=False))
    campaign_end = db.Column(db.TIMESTAMP(timezone=False))

    ad_units = db.relationship('AdUnit', secondary=ad_unit_line_item, backref=db.backref('line_item'))
    creatives = db.relationship('Creative', backref='LineItem', lazy=True)
