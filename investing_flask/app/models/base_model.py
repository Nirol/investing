from datetime import datetime
from typing import Dict, List

from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)

    def updatable_fields_json(self, updatable_fields: List[str]) -> Dict:
        """
        return python dict with only the updatable object fields.
        """
        obj_dict = self.__dict__
        updatable_fields_dict = {}
        for field in updatable_fields:
            field_value = obj_dict.get(field, None)
            if field_value:
                updatable_fields_dict[field] = field_value

        return updatable_fields_dict

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        # do custom initialization here
