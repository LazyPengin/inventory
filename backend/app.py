"""
QR Inventory MVP - Main Application Entry Point
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///qr_inventory.db')
app.config['ALERTS_ENABLED'] = os.getenv('ALERTS_ENABLED', 'false').lower() == 'true'

# Register blueprints
from routes import auth_bp, site_bp, bag_bp, bag_item_bp, qr_bp
app.register_blueprint(auth_bp)
app.register_blueprint(site_bp)
app.register_blueprint(bag_bp)
app.register_blueprint(bag_item_bp)
app.register_blueprint(qr_bp)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'qr-inventory-api',
        'version': '0.1.0'
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'QR Inventory MVP',
        'version': '0.1.0',
        'endpoints': {
            'health': '/health',
            'auth': {
                'login': '/api/auth/login',
                'logout': '/api/auth/logout',
                'me': '/api/auth/me'
            },
            'sites': {
                'create': 'POST /api/sites',
                'list': 'GET /api/sites',
                'get': 'GET /api/sites/<id>',
                'update': 'PATCH /api/sites/<id>',
                'delete': 'DELETE /api/sites/<id>'
            },
            'bags': {
                'create': 'POST /api/sites/<site_id>/bags',
                'list': 'GET /api/sites/<site_id>/bags',
                'get': 'GET /api/bags/<id>',
                'update': 'PATCH /api/bags/<id>',
                'delete': 'DELETE /api/bags/<id>'
            },
            'items': {
                'create': 'POST /api/bags/<bag_id>/items',
                'list': 'GET /api/bags/<bag_id>/items',
                'get': 'GET /api/items/<id>',
                'update': 'PATCH /api/items/<id>',
                'delete': 'DELETE /api/items/<id>'
            },
            'qr': {
                'lookup': 'GET /api/qr/<qr_token>'
            }
        }
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
