from flask import Blueprint, jsonify, request
from models import County, Court

geo_bp = Blueprint("geo", __name__, url_prefix="/api/geo")


@geo_bp.route("/counties", methods=["GET"])
def list_counties():
    """
    List active counties, defaulting to CA.
    GET /api/geo/counties?state=CA
    """
    state = request.args.get("state", "CA")
    counties = (
        County.query
        .filter_by(state=state, is_active=True)
        .order_by(County.name.asc())
        .all()
    )

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "dmvCode": c.dmv_code,
        }
        for c in counties
    ]), 200


@geo_bp.route("/courts", methods=["GET"])
def list_courts():
    """
    List active courts for a given county.
    GET /api/geo/courts?county_id=123
    """
    county_id = request.args.get("county_id", type=int)
    if not county_id:
        return jsonify({"error": "county_id is required"}), 400

    courts = (
        Court.query
        .filter_by(county_id=county_id, is_active=True)
        .order_by(Court.name.asc())
        .all()
    )

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "dmvCode": c.dmv_code,
        }
        for c in courts
    ]), 200
