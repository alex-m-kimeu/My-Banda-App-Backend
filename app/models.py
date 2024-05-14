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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.String)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    quantity = db.Column(db.Integer)
    images = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    reviews = db.relationship('Review', back_populates='product', lazy=True)
    cart_items = db.relationship('Cart', back_populates='product', lazy=True)
    wishlist_items = db.relationship('Wishlist', back_populates='product', lazy=True)
    store = db.relationship('Store', back_populates='products')
    category = db.relationship('Category', back_populates='products')

    #serialize
    serialize_rules = ( ' -reviews.product', '-cart-items.product', '-wishlist_items.product','-store.products','category.products')

    

# Category Model
class Category(db.Model, SerializerMixin):
    __tablename__= 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)
    products = db.relationship('Product', back_populates='category', lazy=True)

    #serialize 
    serialize_rules= ('-products.category')

    
