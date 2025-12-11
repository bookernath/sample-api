"""
BookStore API - A sample REST API demonstrating typical REST principles
Similar to PetStore API with full CRUD operations and OpenAPI specification
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger, swag_from
from datetime import datetime
import uuid
import os

app = Flask(__name__)
CORS(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "BookStore API",
        "description": "A sample REST API demonstrating typical REST principles with books and authors",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@bookstore.example"
        }
    },
    "basePath": "/api/v1",
    "schemes": ["http", "https"],
    "tags": [
        {
            "name": "books",
            "description": "Operations related to books"
        },
        {
            "name": "authors",
            "description": "Operations related to authors"
        },
        {
            "name": "health",
            "description": "Health check operations"
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# In-memory data store
books = {
    "1": {
        "id": "1",
        "title": "The Great Gatsby",
        "author_id": "1",
        "isbn": "978-0-7432-7356-5",
        "published_year": 1925,
        "price": 12.99,
        "stock": 42,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    "2": {
        "id": "2",
        "title": "To Kill a Mockingbird",
        "author_id": "2",
        "isbn": "978-0-06-112008-4",
        "published_year": 1960,
        "price": 14.99,
        "stock": 28,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    "3": {
        "id": "3",
        "title": "1984",
        "author_id": "3",
        "isbn": "978-0-452-28423-4",
        "published_year": 1949,
        "price": 13.99,
        "stock": 35,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
}

authors = {
    "1": {
        "id": "1",
        "name": "F. Scott Fitzgerald",
        "birth_year": 1896,
        "nationality": "American",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    "2": {
        "id": "2",
        "name": "Harper Lee",
        "birth_year": 1926,
        "nationality": "American",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    "3": {
        "id": "3",
        "name": "George Orwell",
        "birth_year": 1903,
        "nationality": "British",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
}


# Health Check Endpoint
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    Health Check
    Returns the health status of the API
    ---
    tags:
      - health
    responses:
      200:
        description: API is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            timestamp:
              type: string
              example: "2024-01-01T00:00:00Z"
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


# Books Endpoints

@app.route('/api/v1/books', methods=['GET'])
def get_books():
    """
    Get all books
    Returns a list of all books with optional filtering
    ---
    tags:
      - books
    parameters:
      - name: author_id
        in: query
        type: string
        required: false
        description: Filter books by author ID
      - name: min_price
        in: query
        type: number
        required: false
        description: Filter books with price greater than or equal to this value
      - name: max_price
        in: query
        type: number
        required: false
        description: Filter books with price less than or equal to this value
    responses:
      200:
        description: List of books
        schema:
          type: object
          properties:
            books:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  title:
                    type: string
                  author_id:
                    type: string
                  isbn:
                    type: string
                  published_year:
                    type: integer
                  price:
                    type: number
                  stock:
                    type: integer
                  created_at:
                    type: string
                  updated_at:
                    type: string
            count:
              type: integer
    """
    author_id = request.args.get('author_id')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    filtered_books = list(books.values())
    
    if author_id:
        filtered_books = [b for b in filtered_books if b['author_id'] == author_id]
    
    if min_price is not None:
        filtered_books = [b for b in filtered_books if b['price'] >= min_price]
    
    if max_price is not None:
        filtered_books = [b for b in filtered_books if b['price'] <= max_price]
    
    return jsonify({
        "books": filtered_books,
        "count": len(filtered_books)
    }), 200


@app.route('/api/v1/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """
    Get a specific book by ID
    Returns details of a single book
    ---
    tags:
      - books
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to retrieve
    responses:
      200:
        description: Book details
        schema:
          type: object
          properties:
            id:
              type: string
            title:
              type: string
            author_id:
              type: string
            isbn:
              type: string
            published_year:
              type: integer
            price:
              type: number
            stock:
              type: integer
            created_at:
              type: string
            updated_at:
              type: string
      404:
        description: Book not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Book not found"
    """
    book = books.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


@app.route('/api/v1/books', methods=['POST'])
def create_book():
    """
    Create a new book
    Adds a new book to the collection
    ---
    tags:
      - books
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - author_id
            - isbn
            - published_year
            - price
          properties:
            title:
              type: string
              example: "The Catcher in the Rye"
            author_id:
              type: string
              example: "1"
            isbn:
              type: string
              example: "978-0-316-76948-0"
            published_year:
              type: integer
              example: 1951
            price:
              type: number
              example: 11.99
            stock:
              type: integer
              example: 50
              default: 0
    responses:
      201:
        description: Book created successfully
        schema:
          type: object
          properties:
            id:
              type: string
            title:
              type: string
            author_id:
              type: string
            isbn:
              type: string
            published_year:
              type: integer
            price:
              type: number
            stock:
              type: integer
            created_at:
              type: string
            updated_at:
              type: string
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    
    # Validation
    required_fields = ['title', 'author_id', 'isbn', 'published_year', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Generate new ID
    book_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    new_book = {
        "id": book_id,
        "title": data['title'],
        "author_id": data['author_id'],
        "isbn": data['isbn'],
        "published_year": data['published_year'],
        "price": data['price'],
        "stock": data.get('stock', 0),
        "created_at": timestamp,
        "updated_at": timestamp
    }
    
    books[book_id] = new_book
    return jsonify(new_book), 201


@app.route('/api/v1/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update an existing book
    Updates all fields of a book (full replacement)
    ---
    tags:
      - books
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - author_id
            - isbn
            - published_year
            - price
          properties:
            title:
              type: string
            author_id:
              type: string
            isbn:
              type: string
            published_year:
              type: integer
            price:
              type: number
            stock:
              type: integer
    responses:
      200:
        description: Book updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
            title:
              type: string
            author_id:
              type: string
            isbn:
              type: string
            published_year:
              type: integer
            price:
              type: number
            stock:
              type: integer
            created_at:
              type: string
            updated_at:
              type: string
      404:
        description: Book not found
        schema:
          type: object
          properties:
            error:
              type: string
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    
    data = request.get_json()
    
    # Validation
    required_fields = ['title', 'author_id', 'isbn', 'published_year', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Preserve original creation timestamp
    created_at = books[book_id]['created_at']
    
    updated_book = {
        "id": book_id,
        "title": data['title'],
        "author_id": data['author_id'],
        "isbn": data['isbn'],
        "published_year": data['published_year'],
        "price": data['price'],
        "stock": data.get('stock', 0),
        "created_at": created_at,
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    books[book_id] = updated_book
    return jsonify(updated_book), 200


@app.route('/api/v1/books/<book_id>', methods=['PATCH'])
def partial_update_book(book_id):
    """
    Partially update a book
    Updates specific fields of a book (partial update)
    ---
    tags:
      - books
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author_id:
              type: string
            isbn:
              type: string
            published_year:
              type: integer
            price:
              type: number
            stock:
              type: integer
    responses:
      200:
        description: Book updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
            title:
              type: string
            author_id:
              type: string
            isbn:
              type: string
            published_year:
              type: integer
            price:
              type: number
            stock:
              type: integer
            created_at:
              type: string
            updated_at:
              type: string
      404:
        description: Book not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    
    data = request.get_json()
    book = books[book_id]
    
    # Update only provided fields
    if 'title' in data:
        book['title'] = data['title']
    if 'author_id' in data:
        book['author_id'] = data['author_id']
    if 'isbn' in data:
        book['isbn'] = data['isbn']
    if 'published_year' in data:
        book['published_year'] = data['published_year']
    if 'price' in data:
        book['price'] = data['price']
    if 'stock' in data:
        book['stock'] = data['stock']
    
    book['updated_at'] = datetime.utcnow().isoformat() + "Z"
    
    return jsonify(book), 200


@app.route('/api/v1/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book
    Removes a book from the collection
    ---
    tags:
      - books
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: The ID of the book to delete
    responses:
      204:
        description: Book deleted successfully
      404:
        description: Book not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    
    del books[book_id]
    return '', 204


# Authors Endpoints

@app.route('/api/v1/authors', methods=['GET'])
def get_authors():
    """
    Get all authors
    Returns a list of all authors
    ---
    tags:
      - authors
    responses:
      200:
        description: List of authors
        schema:
          type: object
          properties:
            authors:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  birth_year:
                    type: integer
                  nationality:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
            count:
              type: integer
    """
    return jsonify({
        "authors": list(authors.values()),
        "count": len(authors)
    }), 200


@app.route('/api/v1/authors/<author_id>', methods=['GET'])
def get_author(author_id):
    """
    Get a specific author by ID
    Returns details of a single author
    ---
    tags:
      - authors
    parameters:
      - name: author_id
        in: path
        type: string
        required: true
        description: The ID of the author to retrieve
    responses:
      200:
        description: Author details
        schema:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            birth_year:
              type: integer
            nationality:
              type: string
            created_at:
              type: string
      404:
        description: Author not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    author = authors.get(author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404
    return jsonify(author), 200


@app.route('/api/v1/authors', methods=['POST'])
def create_author():
    """
    Create a new author
    Adds a new author to the collection
    ---
    tags:
      - authors
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - birth_year
            - nationality
          properties:
            name:
              type: string
              example: "Ernest Hemingway"
            birth_year:
              type: integer
              example: 1899
            nationality:
              type: string
              example: "American"
    responses:
      201:
        description: Author created successfully
        schema:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            birth_year:
              type: integer
            nationality:
              type: string
            created_at:
              type: string
            updated_at:
              type: string
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'birth_year', 'nationality']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Generate new ID
    author_id = str(uuid.uuid4())
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    new_author = {
        "id": author_id,
        "name": data['name'],
        "birth_year": data['birth_year'],
        "nationality": data['nationality'],
        "created_at": timestamp,
        "updated_at": timestamp
    }
    
    authors[author_id] = new_author
    return jsonify(new_author), 201


@app.route('/api/v1/authors/<author_id>', methods=['PUT'])
def update_author(author_id):
    """
    Update an existing author
    Updates all fields of an author
    ---
    tags:
      - authors
    parameters:
      - name: author_id
        in: path
        type: string
        required: true
        description: The ID of the author to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - birth_year
            - nationality
          properties:
            name:
              type: string
            birth_year:
              type: integer
            nationality:
              type: string
    responses:
      200:
        description: Author updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            birth_year:
              type: integer
            nationality:
              type: string
            created_at:
              type: string
            updated_at:
              type: string
      404:
        description: Author not found
        schema:
          type: object
          properties:
            error:
              type: string
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if author_id not in authors:
        return jsonify({"error": "Author not found"}), 404
    
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'birth_year', 'nationality']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Preserve original creation timestamp
    created_at = authors[author_id]['created_at']
    
    updated_author = {
        "id": author_id,
        "name": data['name'],
        "birth_year": data['birth_year'],
        "nationality": data['nationality'],
        "created_at": created_at,
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    authors[author_id] = updated_author
    return jsonify(updated_author), 200


@app.route('/api/v1/authors/<author_id>', methods=['DELETE'])
def delete_author(author_id):
    """
    Delete an author
    Removes an author from the collection
    ---
    tags:
      - authors
    parameters:
      - name: author_id
        in: path
        type: string
        required: true
        description: The ID of the author to delete
    responses:
      204:
        description: Author deleted successfully
      404:
        description: Author not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if author_id not in authors:
        return jsonify({"error": "Author not found"}), 404
    
    del authors[author_id]
    return '', 204


@app.route('/api/v1/authors/<author_id>/books', methods=['GET'])
def get_author_books(author_id):
    """
    Get all books by a specific author
    Returns a list of books written by the specified author
    ---
    tags:
      - authors
    parameters:
      - name: author_id
        in: path
        type: string
        required: true
        description: The ID of the author
    responses:
      200:
        description: List of books by the author
        schema:
          type: object
          properties:
            author:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
            books:
              type: array
              items:
                type: object
            count:
              type: integer
      404:
        description: Author not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    author = authors.get(author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404
    
    author_books = [book for book in books.values() if book['author_id'] == author_id]
    
    return jsonify({
        "author": author,
        "books": author_books,
        "count": len(author_books)
    }), 200


# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """
    API Root
    Welcome message and links to documentation
    ---
    responses:
      200:
        description: Welcome message
        schema:
          type: object
          properties:
            message:
              type: string
            version:
              type: string
            docs:
              type: string
    """
    return jsonify({
        "message": "Welcome to the BookStore API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }), 200


if __name__ == '__main__':
    # Only enable debug mode if explicitly set in environment variable
    # Never use debug=True in production as it exposes the debugger
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
