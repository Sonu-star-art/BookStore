from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship
from app import db

base = declarative_base()


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password, is_admin, phone_number, address):
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.phone_number = phone_number
        self.address = address


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    ISBN = db.Column(db.String, nullable=False, autoincrement=False)  # ISBN contains dashes so it's a string
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, genre, ISBN, price, stock):
        self.title = title
        self.author = author
        self.genre = genre
        self.ISBN = ISBN
        self.price = price
        self.stock = stock


    # When using data in this model in html and js, it's better to have it in the form of a dictionary
    def to_dict(self): 
        return {
            'book_id' : self.book_id,
            'title' : self.title,
            'author' : self.author,
            'genre' : self.genre,
            'ISBN' : self.ISBN,
            'price' : self.price,
            'stock' : self.stock,
        }

    
    def __repr__(self) -> str:
        return f"<User(id={self.book_id}, title='{self.title}', author='{self.author}')>"


class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.String, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_details = db.relationship('OrderDetails', backref="order_ref")  # Order has a one to many relationship with OrderDetails (which itself stores a reference to a book ID and other information)

    def __init__(self, user_id, order_date, total_price, order_details):
        self.user_id = user_id
        self.order_date = order_date
        self.total_price = total_price
        self.order_details = order_details


class OrderDetails(db.Model):
    __tablename__ = "order_details"
    order_details_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, order_id, book_id, quantity):
        self.order_id = order_id
        self.book_id = book_id
        self.quantity = quantity
