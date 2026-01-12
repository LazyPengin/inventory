"""
Site routes - CRUD endpoints for site management
All endpoints require JWT authentication
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from services.site_service import SiteService
from middleware.auth_middleware import require_auth

site_bp = Blueprint('sites', __name__, url_prefix='/api/sites')


def error_response(code: str, message: str, status_code: int):
    """Helper to create consistent error responses"""
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), status_code


@site_bp.route('', methods=['POST'])
@require_auth
def create_site():
    """
    Create a new site
    POST /api/sites
    Auth: Required
    Body: {"name": "...", "alert_recipients": ["email@example.com"]}
    Returns: 201 with site object
    """
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_INPUT', 'Request body must be JSON', 400)
    
    name = data.get('name')
    alert_recipients = data.get('alert_recipients')
    
    if not name:
        return error_response('INVALID_INPUT', 'name is required', 400)
    
    if not alert_recipients:
        return error_response('INVALID_INPUT', 'alert_recipients is required', 400)
    
    db = SessionLocal()
    try:
        site = SiteService.create_site(db, name, alert_recipients)
        return jsonify(SiteService.site_to_dict(site)), 201
    except ValueError as e:
        return error_response('INVALID_INPUT', str(e), 400)
    except Exception as e:
        db.rollback()
        return error_response('INVALID_INPUT', f'Failed to create site: {str(e)}', 400)
    finally:
        db.close()


@site_bp.route('', methods=['GET'])
@require_auth
def list_sites():
    """
    List all sites
    GET /api/sites
    Auth: Required
    Returns: 200 with {"sites": [...]}
    """
    db = SessionLocal()
    try:
        sites = SiteService.get_all_sites(db)
        return jsonify({
            "sites": [SiteService.site_to_dict(site) for site in sites]
        }), 200
    finally:
        db.close()


@site_bp.route('/<int:site_id>', methods=['GET'])
@require_auth
def get_site(site_id: int):
    """
    Get site by ID
    GET /api/sites/<id>
    Auth: Required
    Returns: 200 with site object, 404 if not found
    """
    db = SessionLocal()
    try:
        site = SiteService.get_site_by_id(db, site_id)
        return jsonify(SiteService.site_to_dict(site)), 200
    except ValueError:
        return error_response('NOT_FOUND', 'Site not found', 404)
    finally:
        db.close()


@site_bp.route('/<int:site_id>', methods=['PATCH'])
@require_auth
def update_site(site_id: int):
    """
    Update site (partial update)
    PATCH /api/sites/<id>
    Auth: Required
    Body: {"name": "...", "alert_recipients": [...]} (both optional)
    Returns: 200 with updated site object
    """
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_INPUT', 'Request body must be JSON', 400)
    
    name = data.get('name')
    alert_recipients = data.get('alert_recipients')
    
    # At least one field must be provided
    if name is None and alert_recipients is None:
        return error_response('INVALID_INPUT', 'At least one field (name or alert_recipients) must be provided', 400)
    
    db = SessionLocal()
    try:
        site = SiteService.update_site(db, site_id, name, alert_recipients)
        return jsonify(SiteService.site_to_dict(site)), 200
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg.lower():
            return error_response('NOT_FOUND', error_msg, 404)
        return error_response('INVALID_INPUT', error_msg, 400)
    except Exception as e:
        db.rollback()
        return error_response('INVALID_INPUT', f'Failed to update site: {str(e)}', 400)
    finally:
        db.close()


@site_bp.route('/<int:site_id>', methods=['DELETE'])
@require_auth
def delete_site(site_id: int):
    """
    Delete site
    DELETE /api/sites/<id>
    Auth: Required
    Returns: 204 on success, 409 if site has bags (FK constraint)
    """
    db = SessionLocal()
    try:
        SiteService.delete_site(db, site_id)
        return '', 204
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg.lower():
            return error_response('NOT_FOUND', error_msg, 404)
        return error_response('INVALID_INPUT', error_msg, 400)
    except IntegrityError:
        db.rollback()
        return error_response('CONFLICT', 'Cannot delete site with existing bags', 409)
    except Exception as e:
        db.rollback()
        return error_response('INVALID_INPUT', f'Failed to delete site: {str(e)}', 400)
    finally:
        db.close()
