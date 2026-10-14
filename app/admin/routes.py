from flask import Flask, Blueprint, render_template, url_for, redirect, request, jsonify, flash
from app import db
from . import admin
from models import Book
from app.main.decorators import login_required, admin_required


@admin.route('/update-books')
@login_required
@admin_required
def update_books():
    books = Book.query.all()
    return render_template('updateBooks.html', books=books)


@admin.route('/add-book')
@login_required
@admin_required
def add_book():
    books = Book.query.all()
    return render_template('addBook.html', books=books)


@admin.route('/update-books/edit-book/<int:book_id>')
@login_required
@admin_required
def edit_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    
    return render_template('editBookDetails.html', book=book)


@admin.route('/update-books/edit-book/edit-book-submit', methods=['POST'])
@login_required
@admin_required
def commit_book_changes():
    if request.method == 'POST':
        new_book : dict = request.form
        book : Book = Book.query.filter_by(book_id=new_book['book_id']).first()

        for key, value in new_book.items():
            if type(value) == str:
                value = value.strip()

                if key == 'title' and value != "":
                    book.title = value
                elif key == 'author' and value != "":
                    book.author = value
                elif key == 'genre' and value != "":
                    book.genre = value

                continue
                
            if type(value) == int or type(value) == float:
                if key == 'price' and value >= 0:
                    book.price = value
                elif key == 'stock' and value >= 0:
                    book.stock = value
        
        db.session.commit()

    return redirect(url_for('admin.update_books'))


@admin.route('/add-book/add-book-submit', methods=['POST'])
@login_required
@admin_required
def submit_add_book():
    if request.method == 'POST':
        data : dict = request.form.to_dict()  # make sure it's set to a dictionary, and not 'immutable multi dict' or whatever
        book_data : dict = data

        try:
            for key, value in book_data.items():
                print(key, type(value))

            for key, value in book_data.items():
                if str(value).strip() == "":
                    book_data.pop(key)

            # Convert to numeric
            print(float(book_data['price']))
            book_data['price'] = float(book_data['price']) 
            book_data['stock'] = int(book_data['stock'])

            if book_data['price'] < 0 or book_data['stock'] < 0:
                book_data['title'] += 1

            for key, value in book_data.items():
                print(key, type(value))

            new_book = Book(title=book_data['title'], author=book_data['author'], genre=book_data['genre'], ISBN=book_data['isbn'], price=book_data['price'], stock=book_data['stock'])
            db.session.add(new_book)
            db.session.commit()
        except:
            flash("Couldn't add your book to the database. Something went wrong")
            return redirect(url_for('admin.add_book'))

    return redirect(url_for('admin.update_books'))


@admin.route('/update-books/delete-book', methods=['POST'])
@login_required
@admin_required
def delete_book():
    if request.method == "POST":
        data = request.get_json()

        if data is None:
            return jsonify({ 'success' : False, 'error' : 404})

        book = Book.query.filter_by(book_id=data).first()

        db.session.delete(book)
        db.session.commit()

        return jsonify({'success' : True, 'error' : 200})

    return jsonify({'success' : False, 'error' : 405})
