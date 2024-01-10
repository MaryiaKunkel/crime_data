"""SQLAlchemy models for Crime data."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class Crime(db.Model):
    '''Crimes table'''
    __tablename__='crimes'

    id=db.Column(
        db.Integer, 
        primary_key=True
        )
    
    crime_name=db.Column(
        db.Text, 
        nullable=False, 
        unique=True
        )
    
    location = db.relationship('CrimeLocation', back_populates='crime')

class Location(db.Model):  
    '''Locations table'''
    __tablename__='locations'

    id=db.Column(
        db.Integer, 
        primary_key=True
        )

    latitude=db.Column(
        db.Float,
        nullable=False
    )

    longitude=db.Column(
        db.Float,
        nullable=False
    )

    crime = db.relationship('CrimeLocation', back_populates='location')

class CrimeLocation(db.Model):
    '''Crime-Location table'''
    __tablename__='crime-location'

    id=db.Column(
        db.Integer, 
        primary_key=True
        )

    crime_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'crime.id', 
            ondelete='cascade'
            ),
        nullable=False
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'location.id', 
            ondelete='cascade'
            ),
        nullable=False
    )

    location=db.relationship('Location', back_populates='crime')

    crime = db.relationship('Crime', back_populates='location')

    saved_crimes=db.relationship('SavedCrimes', back_populates='crime_location')

class User(db.Model):
    '''Users table'''
    __tablename__='users'

    id=db.Column(
        db.Integer, 
        primary_key=True
        )
    
    first_name=db.Column(
        db.Text,
        nullable=False,
    )

    last_name=db.Column(
        db.Text,
        nullable=False
    )

    username=db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    email=db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password=db.Column(
        db.Text,
        nullable=False
    )

    saved_crimes=db.relationship('SavedCrimes', back_populates='user')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    
    @classmethod
    def signup(cls, username, email, password):
        """Sign up user. Hashes password and adds user to system."""

        if not username or not email or not password:
            return ("Username, email, and password are required fields")
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class SavedCrimes(db.Model):
    '''Crime-Location table'''
    __tablename__='saved_crimes'

    id=db.Column(
        db.Integer, 
        primary_key=True
        )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'user.id', 
            ondelete='cascade'
            ),
        nullable=False
    )

    crime_loc_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'crime-location.id', 
            ondelete='cascade'
            ),
        nullable=False
    )

    user=db.relationship('User', back_populates='saved_crimes')

    crime_location = db.relationship('CrimeLocation', back_populates='saved_crimes')

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)