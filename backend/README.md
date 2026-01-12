# QR Inventory MVP - Backend

Flask-based REST API for QR Inventory system.

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` as needed (defaults are fine for local development).

5. **Test database connection:**
   ```bash
   python test_connection.py
   ```

6. **Run the server:**
   ```bash
   python app.py
   ```

   Server will start at: http://localhost:5000

### Verify Installation

Test the health check endpoint:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "qr-inventory-api",
  "version": "0.1.0"
}
```

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── database.py            # Database configuration and connection
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── test_connection.py    # Database connection test script
├── migrations/           # Alembic migrations
│   ├── env.py           # Migration environment
│   └── script.py.mako   # Migration template
└── README.md            # This file
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL`: Database connection string (SQLite for dev, PostgreSQL for prod)
- `FLASK_ENV`: development or production
- `FLASK_DEBUG`: Enable debug mode (True/False)
- `PORT`: Server port (default: 5000)
- `ALERTS_ENABLED`: Feature flag for email alerts (default: false)

## Database

### Development
Uses SQLite by default (`qr_inventory.db` in backend directory).

### Production
Configure PostgreSQL connection string in `DATABASE_URL`:
```
postgresql://username:password@host:port/database
```

### Migrations (Coming in DB-1)
Migrations will be added when schema is defined in upcoming tasks.

## API Endpoints

### Health Check
- **GET** `/health`
- Returns service status
- No authentication required

### Root
- **GET** `/`
- Returns API information
- No authentication required

## Next Steps

- **INFRA-2**: Email service integration
- **INFRA-3**: IP geolocation service
- **DB-1**: Core database schema (sites, bags, items)

## Troubleshooting

### Database connection fails
- Check `DATABASE_URL` in `.env`
- Ensure SQLite file has write permissions
- For PostgreSQL, verify server is running and credentials are correct

### Server won't start
- Ensure virtual environment is activated
- Check port 5000 is not in use: `netstat -ano | findstr :5000` (Windows)
- Verify all dependencies installed: `pip install -r requirements.txt`

### Module import errors
- Ensure you're in the `backend` directory
- Verify virtual environment is activated
