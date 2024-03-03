from website.models import User
from website import db

def create_user(email, password):
    user = User(email=email, password=password)
    try :
        db.session.add(user)
        db.session.commit()
        print("User created")
    except:
        print("Error in creating user, organisation or email already exists")
    return user

def read_user(email):
    try:
        return User.query.filter_by(email=email).first()
    except:
        print("Error in reading user")





