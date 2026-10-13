from flask import Flask, Blueprint, render_template, url_for, redirect, request, session, flash, jsonify
#import requests
from app import db
from models import Book, User
from . import main
from app.authentication.routes import submit_login
from app.main.decorators import login_required


@main.route("/")
@login_required
def index():
    return redirect(url_for('auth.login'))


@main.route("/home")
@login_required  # should cause a redirect to login page if user not in session.
def home():

    # When we load the home page, get all the api books again. This is mainly just for testing as it restores books that get deleted by the admin. In the actual application, this would be called just once and never again.
    all_book_data : dict

    try:
        pass
        #response = requests.get(url='https://www.googleapis.com/books/v1/volumes?q=filter=free-ebooks&key=AIzaSyCz4gtMsK7Q4hEumZAUll6xs9ciaSRZyrk')
        #response.raise_for_status()
        #all_book_data : dict = response.json()
    except:
        print("Couldn't get book data")
    
    #add_api_books_to_db(all_book_data['items'])

    user_id = session['user_id']
    user : User = User.query.filter_by(user_id=user_id).first()
    return render_template('home.html', is_admin=user.is_admin)


@main.route("/browse-books")
@login_required
def browse_books():

    books = Book.query.all()
    books_to_dict = []  # A list of books converted to a dictionary

    for book in books:
        books_to_dict.append(book.to_dict())
        print(book.to_dict())

    return render_template('browseBooks.html', books=books_to_dict)

 
# Adds book_id to session cart (this can be called multiple times for a single book to add multiple books to the cart)
@main.route('/browse-books/add-one-book-to-cart/<int:book_id>', methods=['POST'])
@login_required
def add_one_book_to_cart(book_id): 

    print(f"adding book: {book_id} to cart")
    book_id = str(book_id)  # convert to string so it can be for comparing book_id in session (which is a string e.g. '1')

    if request.method == "POST":
        book : Book = Book.query.filter_by(book_id=book_id).first()

        # session book_cart is a dictionary that looks like this { book_id : quantity of books (int) }
        if book is not None:

            # If no books in stock, don't do anything
            if book.stock <= 0:
                flash("No books with that title are in stock.")
                return jsonify({'success' : False, 'error' : 404})  # return 404 not found (since books not in stock)

            if 'book_cart' not in session:
                session['book_cart'] = {}

            # IMPORTANT NOTE: Apparently, flask sessions don't register that you've changed them if you change any sub lists/dicts in it
            # E.g. session['book_cart']['book_quantity'] += 1 Won't change it at all, and this goes for adding new items to sub lists/dicts as well.
            # Instead, you have to do what is done in the code below (break it up into multiple vars and then assign the session to the new session data) 

            # if book_id not in cart, add it id to the cart and set quantity to 1
            if str(book_id) not in session['book_cart']:
                cart = session['book_cart']   
                cart[book_id] = 1
                session['book_cart'] = cart

                #print(f"{book_id} of type: {type(book_id)} IS in session now: {session}")  

            elif session['book_cart'][book_id] < book.stock:  # otherwise increment quantity by 1 (unless it would go over the stock)
                cart = session['book_cart']   
                cart[book_id] += 1
                session['book_cart'] = cart
            else:
                return jsonify({'success' : False, 'message' : "Couldn't add book to cart, because it exceeds the number of books in stock"})
        
        else:
            return jsonify({'success' : False, 'error' : 404})  # return 404 not found (since book matching the input book_id couldn't be found)

    return jsonify({'success' : True})


@main.route('/browse-books/remove-all-books-in-cart', methods=['POST'])
@login_required
def remove_all_books_in_cart():
    print("remove all books in cart")
    if request.method == 'POST':
        if 'book_cart' in session:

            cart : dict = session['book_cart']
            cart.clear()
            session['book_cart'] = cart

            return jsonify({'success' : True, 'error' : 200})

    return jsonify({'success' : False, 'error' : 405})


@main.route('/browse-books/remove-one-book-to-cart/<int:book_id>', methods=['POST'])
@login_required
def remove_one_book_from_cart(book_id):

    book_id = str(book_id)

    if request.method == 'POST':
        book = Book.query.filter_by(book_id=book_id).first()

        if book is not None and 'book_cart' in session and book_id in session['book_cart']:

            # de-increment quantity of books in cart
            cart =  session['book_cart']
            cart[book_id] -= 1
            session['book_cart'] = cart

            if session['book_cart'][book_id] <= 0:  # If it becomes 0 or negative, remove book from cart
                print("delete")
                cart : dict = session['book_cart']
                cart.pop(book_id)
                session['book_cart'] = cart          

                return jsonify({'success' : True, 'message' : "Couldn't remove book because it would exceed 0"})
        else:
            return jsonify({'success' : False, 'error' : 404}) # return 404 not found
    else:
        jsonify({'success' : False, 'error' : 405})  # Server could not understand request (since not POST)


    return jsonify({'success' : True})


@main.route('/browse-books/get-cart', methods=['GET'])
@login_required
def get_session_book_cart(): 

    if request.method == 'GET':
        print("getting data")
        if 'book_cart' not in session:
            return jsonify({'success' : False, 'error' : 404})  # return 404 since book_cart can't be found in session
        
        data = session['book_cart']
        response = jsonify({'book_cart' : data, 'success' : True, 'error' : "none"})
        print(session['book_cart'])
        return response  # this is jsonified 
    
    return jsonify({'success' : False, 'error' : 405})  # return 405 'Method not allowed' if method isn't GET.



def add_api_books_to_db(all_book_data : dict):

    if all_book_data is None:
        return

    filtered_books = []

    for book_data in all_book_data:

        # Some books don't contain ISBN or genre so that's annoying
        isbn = isbn="ISBN is not here, don't ever use it" if 'industryIdentifiers' not in book_data['volumeInfo'] else book_data['volumeInfo']['industryIdentifiers'][0]['identifier']
        genre = genre="Maybe fiction, maybe not" if 'categories' not in book_data['volumeInfo'] else book_data['volumeInfo']['categories'][0]
        author = author="No Author" if 'authors' not in book_data['volumeInfo'] else book_data['volumeInfo']['authors'][0]

        filtered_book_data = {
            "title" : book_data['volumeInfo']['title'],
            "author" : author,  # just get the first author for simplicity
            "genre" : genre,
            "price" : 10.0,  # API doesn't contain price, so I'm making this up
            "ISBN" : isbn,
            "stock" : 5,  # API doesn't contain stock so I'm making this up
        }

        # REMEMBER - NEVER do filtered_books.append(filtered_books) as this will add itself to itelf a bunch of times.
        # When printed, if it looks like this, you've screwed up:
        #[[...], [...], [...], [...], [...], [...], [...], [...], [...], [...]]

        filtered_books.append(filtered_books)

        book_exists = Book.query.filter_by(title=filtered_book_data['title']).first() is not None

        # If book's title already exists in the database, don't add the book to the database
        if book_exists:
            print("book already present")
            continue
        
        # Create book
        book = Book(title=filtered_book_data['title'], author=filtered_book_data['author'], genre=filtered_book_data['genre'],
                    ISBN=filtered_book_data['ISBN'], price=filtered_book_data['price'], stock=filtered_book_data['stock'])
        
        # add book to database
        db.session.add(book)
        db.session.commit()

    
    for book in Book.query.all(): 
        book : Book

        invalid_book_exists = False
        
        # Here, we check if any of the api books DON'T exist (but the book does exist in the database)
        for filtered_book in filtered_books:
            if filtered_book[0] == book.title:
                invalid_book_exists = True
                break
        
        # If the API book no longer exists but it's still in the database, delete it
       # if invalid_book_exists:
       #     print("delete book")
        #    db.session.delete(book)
         #   db.session.commit()
    

@main.route('/order')
@login_required
def order():
    
    # If user hasn't added any books to the cart yet, redirect them to the browse books
    if 'book_cart' not in session or ('book_cart' in session and len(session['book_cart']) == 0):
        flash("Please add a book to cart") # Flash messages require the page to be reloaded (or for a new page to be loaded)
        return redirect(url_for('main.browse_books'))

    cart_data = session['book_cart']

    data = {}  # this is essentially the book model data, plus the quantity in the cart

    for book_id in cart_data:
        book : Book = Book.query.filter_by(book_id=int(book_id)).first()

        data[book_id] = {
            'title' : book.title,
            'author' : book.author,
            'price' : book.price,
            'quantity' : cart_data[book_id], 
        }

    print(data)
    for book in data:
        print(book)

    return render_template('order.html', cart_data=data)


@main.route('/order/process-order', methods=['POST'])
@login_required
def process_order():
    if request.method == 'POST':
        print('processing order')
        data = request.get_json()
    
        if data is None:
            return jsonify({'success' : False, 'error' : 400})  
        else:
            flash("Normally go to payment page. But payment accepted")
            return jsonify({'success' : True, 'error' : 200})

    return jsonify({'success' : False, 'error' : 405})  # return 405 'Method not allowed' if method isn't GET.
