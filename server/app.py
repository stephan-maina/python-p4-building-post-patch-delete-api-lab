#!/usr/bin/env python3
from flask import Flask, jsonify, request
from models import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [book.to_dict() for book in books]
    return jsonify(book_list)

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@app.route('/books/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def manage_book(id):
    book = Book.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(book.to_dict())

    if request.method == 'PATCH':
        data = request.json
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        db.session.commit()
        return jsonify(book.to_dict())

    if request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
