from typing import List, Dict

from marshmallow import Schema, fields

class BaseSchema(Schema):

    @staticmethod
    def is_patch_fields_valid(data:Dict, updateable_fields: List[str]) ->bool:
        """

        :param data: the request payload body.
        :return: if the request payload contain only updatable fields.
        """
        for key in data.keys():
            if key not in updateable_fields:
                return False

        return True

    # common schema fields to all models:
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    id = fields.Integer(dump_only=True)

