"""
Bag routes - CRUD endpoints for bag management
All endpoints require JWT authentication
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from services.bag_service import BagService
from middleware.auth_middleware import require_auth

bag_bp = Blueprint('bags', __name__, url_prefix='/api')


def error_response(code: str, message: str, status_code: int):
    """Helper to create consistent error responses"""
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), status_code


@bag_bp.route('/sites/<int:site_id>/bags', methods=['POST'])
@require_auth
def create_bag(site_id: int):
    """
    Create a new bag with server-generated qr_token
    POST /api/sites/<site_id>/bags
    Auth: Required
    Body: {"name": "..."}
    Returns: 201 with bag object including qr_token
    """
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_INPUT', 'Request body must be JSON', 400)
    
    name = data.get('name')
    
    if not name:
        return error_response('INVALID_INPUT', 'name is required', 400)
    
    # Client cannot provide qr_token (server generates only)
    if 'qr_token' in data:
        return error_response('INVALID_INPUT', 'qr_token cannot be provided by client', 400)
    
    db = SessionLocal()
    try:
        bag = BagService.create_bag(db, site_id, name)
        return jsonify(BagService.bag_to_dict(bag)), 201
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg.lower():
            return error_response('NOT_FOUND', error_msg, 404)
        return error_response('INVALID_INPUT', error_msg, 400)
    except Exception as e:
        db.rollback()
        return error_response('INVALID_INPUT', f'Failed to create bag: {str(e)}', 400)
    finally:
        db.close()


@bag_bp.route('/sites/<int:site_id>/bags', methods=['GET'])
@require_auth
def list_bags_by_site(site_id: int):
    """
    List all bags for a specific site
    GET /api/sites/<site_id>/bags
    Auth: Required
    Returns: 200 with {"bags": [...]}
    """
    db = SessionLocal()
    try:
        bags = BagService.get_bags_by_site(db, site_id)
        return jsonify({
            "bags": [BagService.bag_to_dict(bag) for bag in bags]
        }), 200
    except ValueError as e:
        return error_response('NOT_FOUND', str(e), 404)
    finally:
        db.close()


@bag_bp.route('/bags/<int:bag_id>', methods=['GET'])
@require_auth
def get_bag(bag_id: int):
    """
    Get bag by ID
    GET /api/bags/<id>
    Auth: Required
    Returns: 200 with bag object, 404 if not found
    """
    db = SessionLocal()
    try:
        bag = BagService.get_bag_by_id(db, bag_id)
        return jsonify(BagService.bag_to_dict(bag)), 200
    except ValueError:
        return error_response('NOT_FOUND', 'Bag not found', 404)
    finally:
        db.close()


@bag_bp.route('/bags/<int:bag_id>', methods=['PATCH'])
@require_auth
def update_bag(bag_id: int):
    """
    Update bag (partial update)
    PATCH /api/bags/<id>
    Auth: Required
    Body: {"name": "...", "active": true} (both optional)
    Returns: 200 with updated bag object
    Note: qr_token and site_id are immutable
    """
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_INPUT', 'Request body must be JSON', 400)
    
    # Client cannot modify qr_token or site_id (check immutability first)
    if 'qr_token' in data:
        return error_response('INVALID_INPUT', 'qr_token is immutable and cannot be updated', 400)
    if 'site_id' in data:
        return error_response('INVALID_INPUT', 'site_id is immutable and cannot be updated', 400)
    
    name = data.get('name')
    active = data.get('active')
    
    # At least one field must be provided
    if name is None and active is None:
        return error_response('INVALID_INPUT', 'At least one field (name or active) must be provided', 400)
    
    db = SessionLocal()
    try:
        bag = BagService.update_bag(db, bag_id, name, active)
        return jsonify(BagService.bag_to_dict(bag)), 200
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg.lower():
            return error_response('NOT_FOUND', error_msg, 404)
        return error_response('INVALID_INPUT', error_msg, 400)
    except Exception as e:
        db.rollback()
        return error_response('INVALID_INPUT', f'Failed to update bag: {str(e)}', 400)
    finally:
        db.close()


@bag_bp.route('/bags/<int:bag_id>', methods=['DELETE'])
@require_auth
def delete_bag(bag_id: int):
    """
    Delete bag
    DELETE /api/bags/<id>
    Auth: Required
    Returns: 204 on success, 409 if bag has inventory sessions (FK constraint)
    Note: Cascade deletes bag_items (per DB-1 schema)
    """
    db = SessionLocal()
    try:
        BagService.delete_bag(db, bag_id)
        return '', 204
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg.lower():
            return error_response('NOT_FOUND', error_msg, 404)
        return error_response('INVALID_INPUT', error_msg, 400)
    except IntegrityError:
        db.rollback()
        return error_response('CONFLICT', 'Cannot delete bag with existing inventory sessions', 409)
    except Exception as e:
        db.rollback()
        return error_response('INVALID_INPUT', f'Failed to delete bag: {str(e)}', 400)
    finally:
        db.close()
