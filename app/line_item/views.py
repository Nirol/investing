from flask import Blueprint
from flask import abort, jsonify, request
from marshmallow import ValidationError


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
    db.session.commit()
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
    db.session.commit()
    return line_item_schema.dump(line_item), 201

