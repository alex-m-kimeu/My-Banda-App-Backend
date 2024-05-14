from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import re
from datetime import datetime

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
            raise ValueError("Role must be admin, selller, buyer or deliverer.")
        return role
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 8
        assert re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter"
        assert re.search(r"[a-z]", password), "Password should contain at least one lowercase letter"
        assert re.search(r"[0-9]", password), "Password should contain at lbuyereast one digit"
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
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)  # FK
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)   # FK
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    store = db.relationship('Store', back_populates='complaints')
    buyer = db.relationship('User', back_populates='complaints')

    serialize_rules=('-store.complaint,' '-store.buyer')

    @validates('subject')
    def validate_subject(self, key, subject):
        if not 5 <= len(subject) <= 100:
            raise ValueError("Subject must be between 5 and 100 characters.")
        return subject

    @validates('body')
    def validate_body(self, key, body):
        if not 10 <= len(body) <= 1000:
            raise ValueError("Body must be between 10 and 1000 characters.")
        return body

    pass

# Cart Model
class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # FK

    product = db.relationship('Product', back_populates='cart')
    serialize_rules = ('-product.cart')

    @validates('product_id')
    def validate_product_id(self, key, product_id):
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("Product ID must be a positive integer.")
        return product_id

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
