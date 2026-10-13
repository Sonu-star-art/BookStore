from flask import session, redirect, url_for
from functools import wraps
from models import User



# Is user logged in with session and is logged in user_id in the database
# This function is OVERCOMPLICATED and can be reduced to just 'is user_id in session'
def is_user_logged_in():

    try: 
        user_id = session['user_id']
    except:
        return False

    return 'user_id' in session and session['user_id'] == user_id and User.query.filter_by(user_id=user_id).first() is not None


# Custom decorator. These should typically be put in a dedicated 'decorators.py' file
# and imported into each routes.py file, but I'm keeping it here so I remember it.
def login_required(origninal_function):  # 'original_function' is typically named 'f'
    @wraps(origninal_function)  # remember to do this. I DoN't KnOw WhY... but it prevents an error.
    def decorated_func(*args, **kwargs): 
        if not is_user_logged_in():
            return redirect(url_for('auth.login'))  # If user not logged in, redirect to login
        return origninal_function(*args, **kwargs) # otherwise, run the original function with the same arguments passed into it
    return decorated_func  # technically runs first, as it returns the function inside this function.

    # Note, 'return decorated_func' doesn't have parenthasis after it because that would cause the
    # decorated_func to run immediatey and return whatever is inside it.
    # for decorators, you need to return the decorated_func ITSELF so that it can be called later.



def admin_required(f):
    @wraps(f)
    def decorator_func(*args, **kwargs):
        if 'user_id' in session:
            user : User = User.query.filter_by(user_id=session['user_id']).first()
            if user.is_admin:
                return f(*args, **kwargs)
            return redirect(url_for('main.home')) # if just a regular user, return to home
        return redirect(url_for('auth.login'))
    return decorator_func
        

        

