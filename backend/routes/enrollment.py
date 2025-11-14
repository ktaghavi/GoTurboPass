from flask import Blueprint, request, jsonify
from datetime import datetime

from models.db import db
from models.user import User
from models.student_profile import StudentProfile, GenderEnum, DLClassEnum
from models.citation import Citation
from models.county import County
from models.court import Court

enrollment_bp = Blueprint("enrollment", __name__, url_prefix="/api/enroll")


@enrollment_bp.route("", methods=["POST", "OPTIONS"])
def create_enrollment():
    """
    Phase 1: Create/Update student profile + create citation.

    Expected JSON body:

    {
      "userId": 1,

      "firstName": "Test",
      "lastName": "Student",
      "dob": "1992-05-25",
      "phone": "8183239644",

      // address: we accept either "street" or "addressLine1"
      "street": "123 Main St",
      "city": "Woodland Hills",
      "state": "CA",
      "zip": "91367",

      // driver license
      "dlNumber": "D1234567",
      "dlState": "CA",
      "dlClass": "C",        // A, B, C, M, OTHER

      // optional
      "gender": "MALE",      // MALE, FEMALE, NONBINARY
      "howFound": "ONLINE",

      // citation
      "countyId": 10,
      "courtId": 37,
      "caseNumber": "ABC123456",
      "docketNumber": "XYZ-9999",
      "certificateDueDate": "2025-12-15"   // or "dueDate"
    }
    """

    # --- CORS preflight ---
    if request.method == "OPTIONS":
        return ("", 204)

    if not request.is_json:
        return jsonify({"error": "Expected application/json"}), 415

    data = request.get_json(silent=True) or {}

    # --------- 1. Basic required fields ---------
    user_id = data.get("userId")
    if not user_id:
        return jsonify({"error": "userId is required"}), 400

    required_profile_fields = [
        "firstName", "lastName", "dob", "phone",
        "city", "state", "zip",
        "dlNumber", "dlState", "dlClass",
    ]
    required_citation_fields = [
        "countyId", "courtId", "caseNumber",
    ]

    missing = [
        f for f in (required_profile_fields + required_citation_fields)
        if not data.get(f)
    ]

    # street is special: allow either "street" or "addressLine1"
    street = data.get("street") or data.get("addressLine1")
    if not street:
        missing.append("street")

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "missing": sorted(set(missing)),
        }), 400

    # --------- 2. Look up user / county / court ---------
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    county = County.query.get(data["countyId"])
    if not county:
        return jsonify({"error": "Invalid countyId"}), 400

    court = Court.query.get(data["courtId"])
    if not court or court.county_id != county.id:
        return jsonify({"error": "Invalid courtId for given county"}), 400

    # --------- 3. Parse dates ---------
    try:
        dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid dob format (use YYYY-MM-DD)"}), 400

    # certificate due date: accept certificateDueDate or dueDate or allow None
    cert_due_str = (
        data.get("certificateDueDate")
        or data.get("dueDate")
        or None
    )
    certificate_due_date = None
    if cert_due_str:
        try:
            certificate_due_date = datetime.strptime(cert_due_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid certificate due date format (use YYYY-MM-DD)"}), 400

    # Optional fields
    how_found = data.get("howFound")
    docket_number = data.get("docketNumber")

    # Enums: gender & dl_class
    gender_enum = None
    gender_raw = (data.get("gender") or "").upper().strip()
    if gender_raw:
        try:
            gender_enum = GenderEnum[gender_raw]
        except KeyError:
            return jsonify({
                "error": "Invalid gender value",
                "allowed": [g.name for g in GenderEnum],
            }), 400

    dl_class_raw = (data.get("dlClass") or "").upper().strip()
    try:
        dl_class_enum = DLClassEnum[dl_class_raw]
    except KeyError:
        return jsonify({
            "error": "Invalid dlClass value",
            "allowed": [c.name for c in DLClassEnum],
        }), 400

    try:
        # --------- 4. Upsert StudentProfile ---------
        profile = StudentProfile.query.filter_by(user_id=user.id).first()
        if not profile:
            profile = StudentProfile(user_id=user.id)

        profile.first_name = data["firstName"].strip()
        profile.last_name = data["lastName"].strip()
        profile.dob = dob
        profile.phone = data["phone"].strip()
        profile.street = street.strip()
        profile.city = data["city"].strip()
        profile.state = data["state"].strip()
        profile.zip = data["zip"].strip()

        profile.dl_number = data["dlNumber"].strip()
        profile.dl_state = data["dlState"].strip()
        profile.dl_class = dl_class_enum

        if gender_enum:
            profile.gender = gender_enum

        if how_found:
            profile.how_found = how_found.strip()

        db.session.add(profile)
        db.session.flush()  # assign profile.id if needed

        # --------- 5. Create Citation ---------
        citation = Citation(
            user_id=user.id,
            county_id=county.id,
            court_id=court.id,
            case_number=data["caseNumber"].strip(),
            docket_number=(docket_number or "").strip() or None,
            certificate_due_date=certificate_due_date,
        )

        db.session.add(citation)
        db.session.commit()

        # --------- 6. Audit log (TODO: re-enable when AuditService is added) ---------
        # from services.audit_service import AuditService
        # AuditService.log_event(
        #     event="ENROLL_CREATE",
        #     student_id=user.id,
        #     user_id=user.id,
        #     details={
        #         "county": county.name,
        #         "court": court.name,
        #         "case_number": citation.case_number,
        #     },
        # )

        return jsonify({
            "message": "Enrollment saved successfully",
            "userId": user.id,
            "profileId": profile.id,
            "citationId": citation.id,
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Enrollment failed"}), 500
