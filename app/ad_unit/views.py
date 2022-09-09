from flask import Blueprint
from flask import abort, jsonify, request
from marshmallow import ValidationError
from datetime import datetime

from app.extensions import db
from app.models.ad_unit.ad_unit import AdUnit, AdUnitSchema

ad_units_bp = Blueprint('ad_units', __name__)

@ad_units_bp.route("/ad_unit/list", methods=["GET"])
def get_ad_units():
    schema  = AdUnitSchema(many=True)
    ad_units = AdUnit.query.all()
    return schema.dump(ad_units)


@ad_units_bp.route("/ad_unit/<int:ad_unit_id>", methods=["GET"])
def get_ad_unit(ad_unit_id):
    ad_unit = AdUnit.query.get_or_404(ad_unit_id)
    return AdUnitSchema().dump(ad_unit)


@ad_units_bp.route("/ad_unit/<int:ad_unit_id>", methods=["DELETE"])
def delete_ad_unit(ad_unit_id):
    ad_unit = AdUnit.query.get_or_404(ad_unit_id)
    db.session.delete(ad_unit)
    db.session.commit()
    return jsonify({'result': True})


@ad_units_bp.route('/ad_unit', methods=['POST'])
def create_ad_unit():
    if not request.json:
        abort(400,"no request body")

    try:
        AdUnitSchema().load(request.json)
    except ValidationError as error:
        abort(400,error.messages)

    ad_unit = AdUnit(
        **request.json
    )
    db.session.add(ad_unit)
    db.session.commit()
    return AdUnitSchema().dump(ad_unit), 201


@ad_units_bp.route('/ad_unit/<int:ad_unit_id>', methods=['PATCH'])
def update_ad_unit(ad_unit_id):
    if not request.json:
        abort(400)


    if not AdUnitSchema.is_patch_fields_valid(request.json):
        abort(400,f"Only the fields {AdUnitSchema.UPDATABLE_FIELDS} are updatable")

    ad_unit = AdUnit.query.get_or_404(ad_unit_id)

    for key, value in request.json.items():
        setattr(ad_unit, key, value)

    # validate patched ad unit value:
    try:
        AdUnitSchema().load(ad_unit.updatable_fields_json())
    except ValidationError as error:
        abort(400,error.messages)

    # update the updated_at field:
    ad_unit.updated_at = datetime.utcnow()

    db.session.commit()
    return AdUnitSchema().dump(ad_unit)