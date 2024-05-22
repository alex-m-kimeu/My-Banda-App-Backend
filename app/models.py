from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
import re
from datetime import datetime, timezone
import cloudinary.uploader

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
    contact = db.Column(db.Integer, unique=True, nullable=True)

     # Relationships
    store = db.relationship('Store', back_populates= 'seller', uselist=False, cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates= 'buyer', cascade="all, delete-orphan")
    complaints = db.relationship('Complaint', back_populates= 'buyer', cascade="all, delete-orphan")
    wishlist = db.relationship('Wishlist', back_populates='buyer', cascade="all, delete-orphan")
    cart = db.relationship('Cart', back_populates='buyer', cascade="all, delete-orphan")

    # Serialization rules
    serialize_rules= ('-stores.seller','-reviews', '-complaints',)

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
    
    def upload_image(self, image):
        upload_result = cloudinary.uploader.upload(image)
        self.image = upload_result['url']

# Store Model
class Store(db.Model, SerializerMixin):
    __tablename__= 'stores'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String,nullable=False)
    image = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # Foreign Key
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship
    seller = db.relationship('User', back_populates='store')
    complaints = db.relationship('Complaint', back_populates='store')
    products = db.relationship('Product', back_populates='store')

    # Serialization rules
    serialize_rules= ('-seller','-complaints', '-products.store')

    # validations
    @validates('description')
    def validate_description(self, key, description):
        word_count = len(re.findall(r'\w+', description))
        if word_count < 2 or word_count > 20:
            raise ValueError("Description should be between 2 to 20 words.")
        return description
   
    @validates('location')
    def validate_location(self, key, location):
        word_count = len(re.findall(r'\w+', location))
        if word_count < 1 or word_count > 10:
            raise ValueError("Location should be between 1 to 10 words.")
        return location
    
    def upload_image(self, image):
        upload_result = cloudinary.uploader.upload(image)
        self.image = upload_result['url']

# Complaint Model
class Complaint(db.Model, SerializerMixin):
    __tablename__ = 'complaints'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    # Foreign Keys
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    store = db.relationship('Store', back_populates='complaints')
    buyer = db.relationship('User', back_populates='complaints')

    # Serialization rules
    serialize_rules=('-store', '-buyer.complaint')

    # Validations
    @validates('subject')
    def validate_subject(self, key, subject):
        word_count = len(re.findall(r'\w+', subject))
        if word_count < 2 or word_count > 10:
            raise ValueError("Subject should be between 2 to 10 words.")
        return subject

    @validates('body')
    def validate_body(self, key, body):
        word_count = len(re.findall(r'\w+', body))
        if word_count < 5 or word_count > 150:
            raise ValueError("Body should be between 5 to 150 words.")
        return body
    
    @validates('status')
    def validate_status(self, key, status):
        if status != 'pending' and status != 'resolved' and status != 'rejected':
            raise ValueError("Status must be pending, resolved or rejected.")
        return status
    
# Cart Model
class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    items_cost = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    
    # Foreign Keys
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Relationships
    buyer = db.relationship('User', back_populates='cart', lazy=True) 
    products = db.relationship('Product', back_populates='cart', lazy=True) 
   
    serialize_rules=('-buyer','-products.cart')
    


# Review Model
class Review(db.Model, SerializerMixin):
    __tablename__= 'reviews'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Foreign Keys
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Relationships
    buyer = db.relationship("User", back_populates="reviews")
    product = db.relationship("Product", back_populates="reviews")

    # Serialization rules
    serialize_rules = ('-buyer','-product')

    # Validations
    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    @validates('description')
    def validate_description(self, key , description):
        word_count = len(re.findall(r'\w+', description))
        if word_count < 2 or word_count > 150:
            raise ValueError("Description should be between 2 to 150 words.")
        return description
    
# Wishlist Model
class Wishlist(db.Model, SerializerMixin):
    __tablename__= 'wishlists'

    # Columns
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

 
    # Relationships 
    products = db.relationship('Product', back_populates='wishlist', lazy=True) 
    buyer = db.relationship('User', back_populates='wishlist', lazy=True)
    
    serialize_rules=('-buyer', "-products.wishlist", )

    
# Product Model
class Product(db.Model, SerializerMixin):
    __tablename__= 'products'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    description = db.Column(db.String,nullable=False)
    price = db.Column(db.Float,nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category_name = db.Column(db.String, nullable=False)
    images = db.Column(db.JSON, nullable=False, default=list)

    # Foreign Keys
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    # Relationships
    reviews = db.relationship('Review', back_populates='product', lazy=True)
    store = db.relationship('Store', back_populates='products', lazy=True)
    cart = db.relationship('Cart', back_populates='products', lazy=True) 
    wishlist = db.relationship('Wishlist', back_populates='products', lazy=True) 

    
    # Serialization rules
    serialize_rules = ('-cart', '-wishlist','-store.products', "-reviews.product")

    # Validations
    @validates('title')
    def validate_title(self, key, title):
        word_count = len(re.findall(r'\w+', title))
        if word_count < 1 or word_count > 10:
            raise ValueError("Title should be between 1 to 10 words.")
        return title

    @validates('description')
    def validate_description(self, key, description):
        word_count = len(re.findall(r'\w+', description))
        if word_count < 2 or word_count > 150:
            raise ValueError("Description should be between 5 to 150 words.")
        return description
      
    @validates('category_name')
    def validate_category_name(self, key, category_name):
        allowed_categories = ['Electronics', 'Clothing', 'Shoes', 'Health & beauty','Jewelry']
        if category_name not in allowed_categories:
            raise ValueError("Category name must be one of the following: Electronics, Clothing, Shoes, Health & beauty, Jewelry")
        return category_name

    def upload_images(self, images):
        if self.images is None:
            self.images = []
        for image in images:
            upload_result = cloudinary.uploader.upload(image)
            self.images.append(upload_result['url'])