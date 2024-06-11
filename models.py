from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User in the system."""
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        bcrypt = Bcrypt()

        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf-8")

        return cls(username=username, 
                   password=hashed_pwd, 
                   email=email, 
                   first_name=first_name, 
                   last_name=last_name)


    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False."""

        bcrypt = Bcrypt()
            
        user = User.query.filter_by(username=username).first()
    
        if user and bcrypt.check_password_hash(user.password, pwd):
            # return user instance
            return user
        else:
            return False
        
class Feedback(db.Model):
    """Feedback in the system."""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
    
    user = db.relationship('User', backref='feedback')