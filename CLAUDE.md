# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the API

Start the server:
```bash
python app.py
```

Enable debug mode for development (with auto-reload and detailed errors):
```bash
FLASK_DEBUG=True python app.py
```

The API runs on `http://localhost:5000` and serves Swagger UI documentation at `/api/docs`.

## Architecture

This is a simple Flask REST API demonstrating RESTful principles with two main resources: Books and Authors. The entire application is in `app.py` (single-file architecture).

### Data Storage

Uses in-memory dictionaries (`books` and `authors`) with UUID keys. Data resets on server restart. Both resources include `created_at` and `updated_at` timestamps.

### API Structure

- Base path: `/api/v1`
- All endpoints return JSON
- Uses Flasgger for automatic Swagger UI generation from docstrings
- CORS enabled for all origins

### Key Endpoints

Books:
- `GET /api/v1/books` - Supports query params: `author_id`, `min_price`, `max_price`
- `GET /api/v1/books/{id}`
- `POST /api/v1/books` - Required fields: `title`, `author_id`, `isbn`, `published_year`, `price`. Optional: `stock` (defaults to 0)
- `PUT /api/v1/books/{id}` - Full replacement, requires all fields
- `PATCH /api/v1/books/{id}` - Partial update, updates only provided fields
- `DELETE /api/v1/books/{id}` - Returns 204 on success

Authors:
- `GET /api/v1/authors`
- `GET /api/v1/authors/{id}`
- `POST /api/v1/authors` - Required fields: `name`, `birth_year`, `nationality`
- `PUT /api/v1/authors/{id}` - Requires all fields
- `DELETE /api/v1/authors/{id}` - Returns 204 on success
- `GET /api/v1/authors/{id}/books` - Returns author object with nested books array

Health:
- `GET /api/v1/health` - Returns status and timestamp

### Important Implementation Details

- IDs are generated using `uuid.uuid4()` and stored as strings
- Timestamps use `datetime.utcnow().isoformat() + "Z"` format
- PUT operations preserve the original `created_at` timestamp
- PATCH operations update only the fields present in request body
- Missing required fields return 400 with error message
- Resource not found returns 404 with error message
- Successful creation returns 201 with resource
- Successful deletion returns 204 with empty body

### OpenAPI Specification

The `openapi.yaml` file defines the complete API contract. When modifying endpoints in `app.py`, update both the route docstrings (for Flasgger) and the OpenAPI YAML to keep them in sync.

### Security Note

Debug mode is disabled by default and only enabled via `FLASK_DEBUG` environment variable. Never enable debug mode in production as it exposes the interactive debugger.
