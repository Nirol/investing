from flask import Blueprint
from flask import abort


from app.extensions import db
from app.models import LineItem, LineItemSchema, AdUnit
from flask import request

fetch_bp = Blueprint('fetch', __name__)

@fetch_bp.route("/fetch/line_items", methods=["GET"])
def fetch_line_items():
    FILTER_BY_FIELDS = ["country", "device", "browser", "language", "os"]
    filters = []

    if len(request.args) > 0:
        # dynamically create filters:
        for key,value in request.args.items():
            if key not in FILTER_BY_FIELDS:
                abort(400,f"{key} is invalid search argument")

            filters.append((key,value))
        # conversion to tuple is required to use dynamically created filters
        filters = tuple(filters)


    query = db.session.query(LineItem).join(AdUnit,LineItem.ad_units )


    for _filter, value in filters:
        query = query.filter(getattr(AdUnit, _filter) == value)

    line_items = query.all()
    line_item_schema = LineItemSchema(many=True)
    return line_item_schema.dump(line_items)




