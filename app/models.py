from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import re

db = SQLAlchemy()

# User Model
class User(db.Model, SerializerMixin):
    __tablename__= 'users'
    
    pass

# Store Model
class Store(db.Model, SerializerMixin):
    __tablename__= 'stores'
    
    pass

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

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.Date, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Define relationships
    buyer = db.relationship("Buyer", backref="reviews")
    product = db.relationship("Product", backref="reviews")
    

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
