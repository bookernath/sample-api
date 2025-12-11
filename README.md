# BookStore API

A sample REST API built with Flask, demonstrating typical REST principles similar to the PetStore API. This API provides a complete CRUD interface for managing books and authors with comprehensive OpenAPI/Swagger documentation.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Multiple HTTP verbs (GET, POST, PUT, PATCH, DELETE)
- ✅ RESTful design principles
- ✅ Query parameter filtering
- ✅ OpenAPI 3.0 specification
- ✅ Interactive Swagger UI documentation
- ✅ CORS enabled
- ✅ Proper HTTP status codes
- ✅ In-memory data storage

## API Resources

### Books
Manage a collection of books with the following operations:
- `GET /api/v1/books` - List all books (with optional filtering)
- `GET /api/v1/books/{id}` - Get a specific book
- `POST /api/v1/books` - Create a new book
- `PUT /api/v1/books/{id}` - Update a book (full replacement)
- `PATCH /api/v1/books/{id}` - Partially update a book
- `DELETE /api/v1/books/{id}` - Delete a book

### Authors
Manage a collection of authors:
- `GET /api/v1/authors` - List all authors
- `GET /api/v1/authors/{id}` - Get a specific author
- `POST /api/v1/authors` - Create a new author
- `PUT /api/v1/authors/{id}` - Update an author
- `DELETE /api/v1/authors/{id}` - Delete an author
- `GET /api/v1/authors/{id}/books` - Get all books by an author

### Health Check
- `GET /api/v1/health` - Check API health status

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/bookernath/sample-api.git
cd sample-api
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the Flask development server:
```bash
python app.py
```

The API will be available at: `http://localhost:5000`

### Development Mode

For development with debug mode enabled (provides detailed error messages and auto-reload):
```bash
FLASK_DEBUG=True python app.py
```

**Warning:** Never use debug mode in production as it exposes the interactive debugger which can be a security risk.

## API Documentation

Once the server is running, access the interactive Swagger UI documentation at:
```
http://localhost:5000/api/docs
```

The OpenAPI specification is also available as a standalone file: `openapi.yaml`

## Usage Examples

### Get all books
```bash
curl http://localhost:5000/api/v1/books
```

### Get a specific book
```bash
curl http://localhost:5000/api/v1/books/1
```

### Filter books by price range
```bash
curl "http://localhost:5000/api/v1/books?min_price=10&max_price=15"
```

### Create a new book
```bash
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Catcher in the Rye",
    "author_id": "1",
    "isbn": "978-0-316-76948-0",
    "published_year": 1951,
    "price": 11.99,
    "stock": 50
  }'
```

### Update a book (full replacement)
```bash
curl -X PUT http://localhost:5000/api/v1/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby - Updated",
    "author_id": "1",
    "isbn": "978-0-7432-7356-5",
    "published_year": 1925,
    "price": 15.99,
    "stock": 30
  }'
```

### Partially update a book
```bash
curl -X PATCH http://localhost:5000/api/v1/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 9.99,
    "stock": 100
  }'
```

### Delete a book
```bash
curl -X DELETE http://localhost:5000/api/v1/books/1
```

### Get all books by an author
```bash
curl http://localhost:5000/api/v1/authors/1/books
```

## REST Principles Demonstrated

1. **Resource-Based URLs**: Clear, noun-based endpoints (`/books`, `/authors`)
2. **HTTP Methods**: Proper use of GET, POST, PUT, PATCH, DELETE
3. **Status Codes**: Appropriate HTTP status codes (200, 201, 204, 400, 404)
4. **Stateless**: Each request contains all necessary information
5. **JSON Format**: Standard JSON for request/response bodies
6. **Query Parameters**: Filtering and pagination support
7. **Relationships**: Author-to-books relationship endpoint
8. **Idempotency**: PUT and DELETE operations are idempotent

## HTTP Methods Explained

- **GET**: Retrieve resource(s) - Safe and idempotent
- **POST**: Create new resource - Not idempotent
- **PUT**: Replace entire resource - Idempotent
- **PATCH**: Partially update resource - Not necessarily idempotent
- **DELETE**: Remove resource - Idempotent

## Sample Data

The API comes pre-loaded with sample data:

**Books:**
- The Great Gatsby by F. Scott Fitzgerald
- To Kill a Mockingbird by Harper Lee
- 1984 by George Orwell

**Authors:**
- F. Scott Fitzgerald
- Harper Lee
- George Orwell

## Project Structure

```
sample-api/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── openapi.yaml        # OpenAPI 3.0 specification
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Technologies Used

- **Flask**: Lightweight WSGI web application framework
- **Flask-CORS**: Handle Cross-Origin Resource Sharing
- **Flasgger**: Flask extension for automatic Swagger UI generation

## Development

### Adding New Resources

To add a new resource:
1. Define the data model in the in-memory store
2. Create CRUD endpoints following REST conventions
3. Add OpenAPI documentation in docstrings
4. Update the OpenAPI YAML file

### Data Persistence

Currently, this API uses in-memory storage. Data is lost when the server restarts. For production use, consider integrating:
- SQLite for simple file-based persistence
- PostgreSQL/MySQL for full-featured database
- MongoDB for document-based storage

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub.