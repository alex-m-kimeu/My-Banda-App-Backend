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
