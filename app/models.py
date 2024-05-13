from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import re

db = SQLAlchemy()

# User Model
class User(db.Model, SerializerMixin):
    __tablename__= 'users'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    contact = db.Column(db.Integer, nullable=False)

     # relationships with store, review and complaint model
    store = db.relationship('Store', back_populates= 'seller', uselist=False, cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates= 'buyer', cascade="all, delete-orphan")
    complaints = db.relationship('Complaint', back_populates= 'buyer', cascade="all, delete-orphan")

    # serialization rules
    serialize_rules= ('-stores.seller','-reviews.buyer', '-complaints.buyer',)

    # validations
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Invalid email format"
        return email
    

    @validates('role')
    def validate_role(self, key, role):
        if role != 'admin' and role != 'seller' and role != 'buyer' and role != 'deliverer':
            raise ValueError("Role must be admin, seller, buyer or deliverer.")
        return role
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 8
        assert re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter"
        assert re.search(r"[a-z]", password), "Password should contain at least one lowercase letter"
        assert re.search(r"[0-9]", password), "Password should contain at least one digit"
        assert re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password should contain at least one special character"
        return password
    
    def __repr__(self):
        return f"<User {self.id}, {self.username}, {self.contact},{self.image},{self.role}, {self.email}, {self.password}>"
    

# Store Model
class Store(db.Model, SerializerMixin):
    __tablename__= 'stores'

    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String,nullable=False)
    image = db.Column(db.String, nullable=True)
    location = db.Column(db.String)

    # Foreign Key
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with seller and complaints
    seller = db.relationship('User', back_populates='store')
    complaints = db.relationship('Complaint', back_populates='store')
    products = db.relationship('Product', back_populates='store')

    # serialization rules
    serialize_rules= ('-seller.store','-complaints.store',)

    # validation
    @validates('description')
    def validate_description(self, key, description):
         if not 5 <= len(description) <= 150:
             raise ValueError("Description must be between 5 and 150 characters.")
         return description




# Complaint Model
class Complaint(db.Model, SerializerMixin):
    __tablename__= 'complaints'
    
    pass

# Cart Model
class Cart(db.Model, SerializerMixin):
    __tablename__= 'carts'
    
    pass

# Review Model
class Review(db.Model, SerializerMixin):
    __tablename__= 'reviews'
    
    pass

# Wishlist Model
class Wishlist(db.Model, SerializerMixin):
    __tablename__= 'wishlists'
    
    pass

# Product Model
class Product(db.Model, SerializerMixin):
    __tablename__= 'products'
    
    pass

# Category Model
class Category(db.Model, SerializerMixin):
    __tablename__= 'categories'
    
    pass
