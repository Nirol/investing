from flask import Blueprint
from flask import abort, jsonify, request
from marshmallow import ValidationError
from datetime import datetime

from sqlalchemy.exc import IntegrityError, ProgrammingError

from app.extensions import db
from app.models import Creative, CreativeSchema

creative_bp = Blueprint("creative", __name__)


@creative_bp.route("/creative/list", methods=["GET"])
def get_creatives():
    creative_schema = CreativeSchema(many=True)
    creatives = Creative.query.all()
    return creative_schema.dump(creatives)


@creative_bp.route("/creative/<int:creative_id>", methods=["GET"])
def get_creative(creative_id):
    creative = Creative.query.get_or_404(creative_id)
    return CreativeSchema().dump(creative)


@creative_bp.route("/creative/<int:creative_id>", methods=["DELETE"])
def delete_creative(creative_id):
    creative = Creative.query.get_or_404(creative_id)
    db.session.delete(creative)
    try:
        db.session.commit()
    except IntegrityError as error:
        abort(400, error)
    return jsonify({"result": True})


@creative_bp.route("/creative", methods=["POST"])
def create_creative():
    creative_schema = CreativeSchema()
    if not request.json:
        abort(400, "no request body")

    try:
        creative_dict = creative_schema.load(request.json)
    except ValidationError as error:
        abort(400, error.messages)

    creative = Creative(**creative_dict)
    db.session.add(creative)
    try:
        db.session.commit()
    except IntegrityError or ProgrammingError as error:
        abort(400, error)
    return creative_schema.dump(creative), 201


@creative_bp.route("/creative/<int:creative_id>", methods=["PATCH"])
def patch_creative(creative_id):
    if not request.json:
        abort(400)
    creative_schema = CreativeSchema()

    if not CreativeSchema.is_patch_fields_valid(
        data=request.json, updateable_fields=CreativeSchema.CREATIVE_UPDATABLE_FIELDS
    ):
        abort(400, f"Only the fields {CreativeSchema.CREATIVE_UPDATABLE_FIELDS} are updatable")

    creative = Creative.query.get_or_404(creative_id)

    for key, value in request.json.items():
        setattr(creative, key, value)

    # validate patched creative values:
    try:
        creative_schema.load(creative.updatable_fields_json(updatable_fields=CreativeSchema.CREATIVE_UPDATABLE_FIELDS))
    except ValidationError as error:
        abort(400, error.messages)

    # update the updated_at field:
    creative.updated_at = datetime.utcnow()

    try:
        db.session.commit()
    except IntegrityError as error:
        abort(400, error)
    return creative_schema.dump(creative)


@creative_bp.route("/creative/<int:creative_id>", methods=["PUT"])
def put_creative(creative_id):
    if not request.json:
        abort(400)
    creative_schema = CreativeSchema()

    try:
        # as in POST request, the payload need to hold all required line item arguments.
        creative_schema.load(request.json)
    except ValidationError as error:
        abort(400, error.messages)

    creative = Creative.query.get_or_404(creative_id)

    for key, value in request.json.items():
        setattr(creative, key, value)

    # validate patched line item value:
    try:
        creative_schema.load(creative.updatable_fields_json(updatable_fields=CreativeSchema.CREATIVE_UPDATABLE_FIELDS))
    except ValidationError as error:
        abort(400, error.messages)

    # update the updated_at field:
    creative.updated_at = datetime.utcnow()

    db.session.commit()
    return creative_schema.dump(creative)
