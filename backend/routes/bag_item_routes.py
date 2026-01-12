"""
BagItem routes - admin-protected CRUD endpoints for bag items
"""
from flask import Blueprint, request, jsonify
from database import SessionLocal
from middleware.auth_middleware import require_auth
from services.bag_item_service import BagItemService

bag_item_bp = Blueprint('bag_items', __name__)


def error_response(code: str, message: str, status_code: int):
    """Helper to create consistent error responses"""
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), status_code


@bag_item_bp.route('/api/bags/<int:bag_id>/items', methods=['POST'])
@require_auth
def create_item(bag_id):
    """
    Create a new item for a bag.
    
    POST /api/bags/:bag_id/items
    Body: {name, expected_qty?, track_expiry?, expiry_date?, test_batteries?}
    
    Returns:
        201: item created
        400: validation error
        401: unauthorized
        404: bag not found
    """
    data = request.get_json()
    if not data:
        return error_response('INVALID_INPUT', 'request body is required', 400)
    
    db = SessionLocal()
    try:
        item = BagItemService.create_bag_item(db, bag_id, data)
        return jsonify(BagItemService.bag_item_to_dict(item)), 201
    
    except KeyError as e:
        return error_response('NOT_FOUND', str(e), 404)
    
    except ValueError as e:
        return error_response('INVALID_INPUT', str(e), 400)
    
    finally:
        db.close()


@bag_item_bp.route('/api/bags/<int:bag_id>/items', methods=['GET'])
@require_auth
def list_items(bag_id):
    """
    List all items for a bag.
    
    GET /api/bags/:bag_id/items
    
    Returns:
        200: {items: [...]}
        401: unauthorized
        404: bag not found
    """
    db = SessionLocal()
    try:
        items = BagItemService.get_bag_items(db, bag_id)
        return jsonify({
            'items': [BagItemService.bag_item_to_dict(item) for item in items]
        }), 200
    
    except ValueError as e:
        return error_response('NOT_FOUND', str(e), 404)
    
    finally:
        db.close()


@bag_item_bp.route('/api/items/<int:item_id>', methods=['GET'])
@require_auth
def get_item(item_id):
    """
    Get a single item by ID.
    
    GET /api/items/:id
    
    Returns:
        200: item data
        401: unauthorized
        404: item not found
    """
    db = SessionLocal()
    try:
        item = BagItemService.get_bag_item_by_id(db, item_id)
        return jsonify(BagItemService.bag_item_to_dict(item)), 200
    
    except KeyError as e:
        return error_response('NOT_FOUND', str(e), 404)
    
    finally:
        db.close()


@bag_item_bp.route('/api/items/<int:item_id>', methods=['PATCH'])
@require_auth
def update_item(item_id):
    """
    Update an item (partial update).
    
    PATCH /api/items/:id
    Body: {name?, expected_qty?, track_expiry?, expiry_date?, test_batteries?}
    
    Returns:
        200: updated item
        400: validation error
        401: unauthorized
        404: item not found
    """
    data = request.get_json()
    if not data:
        return error_response('INVALID_INPUT', 'request body is required', 400)
    
    db = SessionLocal()
    try:
        item = BagItemService.update_bag_item(db, item_id, data)
        return jsonify(BagItemService.bag_item_to_dict(item)), 200
    
    except KeyError as e:
        return error_response('NOT_FOUND', str(e), 404)
    
    except ValueError as e:
        return error_response('INVALID_INPUT', str(e), 400)
    
    finally:
        db.close()


@bag_item_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
@require_auth
def delete_item(item_id):
    """
    Delete an item.
    
    DELETE /api/items/:id
    
    Per DB-1: inventory_results.bag_item_id has ON DELETE SET NULL,
    so delete always succeeds even if results exist.
    
    Returns:
        204: deleted successfully
        401: unauthorized
        404: item not found
    """
    db = SessionLocal()
    try:
        BagItemService.delete_bag_item(db, item_id)
        return '', 204
    
    except KeyError as e:
        return error_response('NOT_FOUND', str(e), 404)
    
    finally:
        db.close()
