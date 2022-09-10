from flask import Blueprint
from flask import abort, jsonify, request
from marshmallow import ValidationError
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.line_item.line_item import LineItem, LineItemSchema

line_item_bp = Blueprint('line_item', __name__)

@line_item_bp.route("/line_item/list", methods=["GET"])
def get_line_items():
    line_item_schema  = LineItemSchema(many=True)
    line_items = LineItem.query.all()
    return line_item_schema.dump(line_items)


@line_item_bp.route("/line_item/<int:line_item_id>", methods=["GET"])
def get_line_item(line_item_id):
    line_item = LineItem.query.get_or_404(line_item_id)
    return LineItemSchema().dump(line_item)


@line_item_bp.route("/line_item/<int:line_item_id>", methods=["DELETE"])
def delete_line_item(line_item_id):
    line_item = LineItem.query.get_or_404(line_item_id)
    db.session.delete(line_item)
    try:
        db.session.commit()
    except IntegrityError as error:
        abort(400, error)
    return jsonify({'result': True})


@line_item_bp.route('/line_item', methods=['POST'])
def create_line_item():
    line_item_schema = LineItemSchema()
    if not request.json:
        abort(400,"no request body")

    try:
        line_item_dict= line_item_schema.load(request.json)
    except ValidationError as error:
        abort(400,error.messages)

    line_item = LineItem(
        **line_item_dict
    )

    db.session.add(line_item)
    try:
        db.session.commit()
    except IntegrityError as error:
        abort(400, error)
    return line_item_schema.dump(line_item), 201


@line_item_bp.route('/line_item/<int:line_item_id>', methods=['PATCH'])
def patch_line_item(line_item_id):
    if not request.json:
        abort(400)
    line_item_schema = LineItemSchema()

    if not LineItemSchema.is_patch_fields_valid(data=request.json, updateable_fields=LineItemSchema.LINE_ITEM_UPDATABLE_FIELDS):
        abort(400,f"Only the fields {LineItemSchema.LINE_ITEM_UPDATABLE_FIELDS} are updatable")

    line_item = LineItem.query.get_or_404(line_item_id)

    for key, value in request.json.items():
        setattr(line_item, key, value)

    # validate patched line_item values:
    try:
        line_item_dict = line_item_schema.load(line_item.updatable_fields_json(updatable_fields=LineItemSchema.LINE_ITEM_UPDATABLE_FIELDS))
    except ValidationError as error:
        abort(400,error.messages)

    if "ad_unit_ids" in request.json:
        # if ad_unit_ids were updated, line_item_dict will hold the updated AdUnit objects
        line_item.ad_units =  line_item_dict['ad_units']

    # update the updated_at field:
    line_item.updated_at = datetime.utcnow()

    try:
        db.session.commit()
    except IntegrityError as error:
        abort(400, error)
    return line_item_schema.dump(line_item)


@line_item_bp.route('/line_item/<int:line_item_id>', methods=['PUT'])
def put_line_item(line_item_id):
    if not request.json:
        abort(400)
    line_item_schema = LineItemSchema()

    try:
        # as in POST request, the payload need to hold all required line item arguments.
        line_item_schema.load(request.json)
    except ValidationError as error:
        abort(400,error.messages)


    line_item = LineItem.query.get_or_404(line_item_id)

    for key, value in request.json.items():
        setattr(line_item, key, value)

    # validate patched line item value:
    try:
        line_item_dict = line_item_schema.load(line_item.updatable_fields_json(updatable_fields=LineItemSchema.LINE_ITEM_UPDATABLE_FIELDS))
    except ValidationError as error:
        abort(400,error.messages)

    if "ad_unit_ids" in request.json:
        # if ad_unit_ids were updated, line_item_dict will hold the updated AdUnit objects
        line_item.ad_units =  line_item_dict['ad_units']

    # update the updated_at field:
    line_item.updated_at = datetime.utcnow()

    db.session.commit()
    return line_item_schema.dump(line_item)