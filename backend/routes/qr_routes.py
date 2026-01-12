"""
QR routes - Public endpoint for QR token lookup
No authentication required (anonymous endpoint)
"""
from flask import Blueprint, jsonify
from database import SessionLocal
from services.qr_service import QRService

qr_bp = Blueprint('qr', __name__)


def error_response(code: str, message: str, status_code: int):
    """Helper to create consistent error responses"""
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), status_code


@qr_bp.route('/api/qr/<qr_token>', methods=['GET'])
def lookup_qr(qr_token):
    """
    Look up a bag by QR token (public endpoint).
    
    GET /api/qr/<qr_token>
    
    Returns:
        200: {bag: {...}, items: [...]}
        404: bag not found or inactive
    """
    db = SessionLocal()
    try:
        result = QRService.lookup_by_qr_token(db, qr_token)
        return jsonify(result), 200
    
    except ValueError as e:
        # Both "not found" and "inactive" return 404 to avoid info leakage
        return error_response('NOT_FOUND', str(e), 404)
    
    finally:
        db.close()
