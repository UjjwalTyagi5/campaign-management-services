# FastAPI Campaign Management Backend

An backend API for managing discount campaigns and customers, built with FastAPI, SQLAlchemy, and SQLite. Includes Docker support for easy deployment.

## Features
- CRUD for campaigns and customers
- Assign discounts to cart or delivery
- Set campaign duration and budget
- Restrict discount usage per customer per day
- Target specific customers
- Fetch available campaigns for a customer
- API docs via Swagger UI
- Logging with Loguru
- Organized codebase (routes, dependencies, schemas)
- Dockerized for production

## Tech Stack
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Loguru
- Docker

## Project Structure
```
backend/
├── api/                # Routes, dependencies, schemas
├── app/                # Log files
├── core/               # Config, logger
├── db/                 # Database models, connection
├── main.py             # App entrypoint
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build file
├── entrypoint.sh       # Docker entrypoint script
└── campaigns.db        # SQLite database file
```

## Getting Started

### Local Development
### Create virtual environment befor this step
1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
2. Run the app:
   ```cmd
   python main.py
   or 

   ```
3. Open API docs:
   [http://localhost:8000/docs](http://localhost:8000/docs)

### Docker
1. Build the image:
   ```powershell
   docker build -t fastapi-campaigns .
   ```
2. Run the container:
   ```powershell
  docker run -p 8000:8000 fastapi-campaigns start-api-server
   ```

## Main API Endpoints
- `POST /campaigns/` - Create campaign
- `GET /campaigns/` - List campaigns
- `GET /campaigns/available` - Get available campaigns for a customer
- `GET /campaigns/{campaign_id}` - Get campaign by ID
- `PATCH /campaigns/{campaign_id}` - Update campaign (partial)
- `DELETE /campaigns/{campaign_id}` - Delete campaign
- `POST /customers/` - Create customer
- `GET /customers/` - List customers
- `GET /customers/{customer_id}` - Get customer by ID
- `PUT /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer
- `GET /health/` - Health check

## Environment & Logging
- Optional `.env` for config
- Logs stored in `app/` by date

## Extending
- Add endpoints in `api/routes/`
- Add business logic in `api/dependencies/`
- Update `entrypoint.sh` for more services

