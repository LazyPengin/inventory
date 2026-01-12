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
        'endpoints': {
            'health': '/health'
        }
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
