from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv
import os

from models import db, User, Store, Complaint, Cart, Review, Wishlist, Product, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Hardcode Admin Credentials
def create_admin():
    admin_email = "banda.admin@gmail.com"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        hashed_password = bcrypt.generate_password_hash("Admin123!").decode('utf-8')
        admin = User(
            username="My Banda", 
            email=admin_email,
            role="admin",
            password=hashed_password,
            contact="1234567890",
            image="https://images.pexels.com/photos/12814838/pexels-photo-12814838.png?auto=compress&cs=tinysrgb&w=600"
        )
        db.session.add(admin)
        db.session.commit()

# Restful Routes
# Sign in
class SignIn(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return {"error": "User does not exist"}, 401
        if not bcrypt.check_password_hash(user.password, password):
            return {"error": "Incorrect password"}, 401
        
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        refresh_token = create_refresh_token(identity={'id': user.id, 'role': user.role})
        return {"access_token": access_token, "refresh_token": refresh_token}, 200

api.add_resource(SignIn, '/signin')

# Sign up
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            username=data['username'], 
            email=data['email'],
            role=data['role'],
            password=hashed_password
            # contact=data['contact'],
            # image=data['image']
            )
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        refresh_token = create_refresh_token(identity={'id': user.id, 'role': user.role})
        return make_response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }, 201)

api.add_resource(SignUp, '/signup')

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return {'access_token': access_token}, 200
        except Exception as e:
            return jsonify(error=str(e)), 500

api.add_resource(TokenRefresh, '/refresh-token')

# USERS (get post)
class Users(Resource):
    @jwt_required()
    def get(self):        
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users,200)
      
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
    
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            username=data['username'], 
            email=data['email'],
            role=data['role'],
            password=hashed_password
            # contact=data['contact'],
            # image=data['image']
            )
        
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 201)
    
api.add_resource(Users, '/users')


# Routes for Products
class Products(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        if claims['role'] != 'seller' and claims['role'] != 'buyer':
            return {"error": "Only sellers and buyers can view products"}, 403
        
        products = [product.to_dict() for product in Product.query.all()]
        return make_response(products, 200)

    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can post new products"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        title = data.get('title')
        description = data.get('description')
        store_id = data.get('store_id')
        price = data.get('price')
        quantity = data.get('quantity')
        category_id = data.get('category_id')
        images=data.get('images')

        # Validate input data
        # if not all([title, description, seller_id, price, quantity, category_id]):
        #     return {"error": "Missing required fields"}, 400

        # seller = User.query.get(seller_id)
        # category = Category.query.get(category_id)

        # if not seller:
        #     return {"error": "Seller not found"}, 404

        # if not category:
        #     return {"error": "Category not found"}, 404

        product = Product(
            title=title,
            description=description,
            store_id=store_id,
            price=price,
            quantity=quantity,
            category_id=category_id,
            images=images
        )

        db.session.add(product)
        db.session.commit()
        return make_response(product.to_dict(), 201)


api.add_resource(Products, '/products')

class ProductsByID(Resource):
    @jwt_required()
    def get(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'seller' and claims['role'] != 'buyer':
            return {"error": "Only sellers and buyers can view products"}, 403
        
        product = Product.query.get(id)
        if product:
            return make_response(product.to_dict(), 200)
        else:
            return {"error": "Product not found"}, 404

    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can edit products"}, 403
        
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        data = request.get_json()

        # Validate input data
        # if not data:
        #     return {"error": "Missing data in request"}, 400

        # valid_fields = ['title', 'description', 'seller_id', 'price', 'quantity', 'category_id']
        # if not all(field in data for field in valid_fields):
        #     return {"error": "Missing or invalid fields in request"}, 400

        # seller = User.query.get(data.get('seller_id'))
        # category = Category.query.get(data.get('category_id'))

        # if not seller:
        #     return {"error": "Seller not found"}, 404

        # if not category:
        #     return {"error": "Category not found"}, 404

        product.title = data.get('title')
        product.description = data.get('description')
        product.store_id = data.get('store_id')
        product.price = data.get('price')
        product.quantity = data.get('quantity')
        product.category_id = data.get('category_id')
        product.images = data.get('images')

        db.session.commit()
        return make_response(product.to_dict(), 200)

    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can delete products"}, 403
        
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200


api.add_resource(ProductsByID, '/products/<int:id>')

# User By ID (get patch delete)
class UserByID(Resource):
    @jwt_required()
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error": "User not found"}, 404
        response_dict = user.to_dict()
        return make_response(response_dict, 200)
    
    @jwt_required()
    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error": "User not found"}, 404
        
        data = request.get_json()
        if all(key in data for key in ['username', 'email', 'password', 'contact']):
            try:   
                user.username = data['username']
                user.email = data['email']
                user.contact = data['contact']
                user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                db.session.commit()
                return make_response(user.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400

    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin':
            return {"error": "Only admin can remove users"}, 403
              
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error": "User not found"}, 404
        
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return make_response({'message': 'User deleted successfully'})
    
api.add_resource(UserByID, '/user/<int:id>')

# STORE (get post)
class Stores(Resource):
    @jwt_required()
    def get(self):
        stores = [store.to_dict() for store in Store.query.all()]
        return make_response(stores,200)
        
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can create stores"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
    
        store = Store(
            store_name=data['store_name'], 
            description=data['description'],
            image=data['image'],
            location=data['location'],
            seller_id=data['seller_id']
            )
        
        db.session.add(store)
        db.session.commit()
        return make_response(store.to_dict(), 201)


api.add_resource(Stores, '/stores')

# Store By ID (get patch delete)
class StoreByID(Resource):
    @jwt_required()
    def get(self,id):
        store = Store.query.filter_by(id=id).first()
        if store is None:
            return {"error": "Store not found"}, 404
        response_dict = store.to_dict()
        return make_response(response_dict, 200)
    
    @jwt_required()
    def patch(self,id):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can edit a store"}, 403
        
        store = Store.query.filter_by(id=id).first()
        if store is None:
            return {"error": "Store not found"}, 404
        
        data = request.get_json()
        if all(key in data for key in ['store_name', 'description', 'image', 'location']):
            try:   
                store.store_name = data['store_name']
                store.description= data['description']
                store.image = data['image']
                store.location = data['location']
                db.session.commit()
                return make_response(store.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400

    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can remove a store"}, 403
             
        store = Store.query.filter_by(id=id).first()
        if store is None:
            return {"error": "Store not found"}, 404
        
        store = Store.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()
        return make_response({'message': 'Store deleted successfully'})
    
api.add_resource(StoreByID, '/store/<int:id>')

#Route for Categories
class Categories(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        if claims['role'] != 'seller' and claims['role'] != 'buyer':
            return {"error": "Only sellers and buyers can view categories"}, 403
        
        categories = [category.to_dict() for category in Category.query.all()]
        return make_response(categories, 200)

    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can add categories"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        # category_name = data['category_name']
        # if not category_name:
        #     return {"error": "Missing category name"}, 400

        # category = Category(category_name=category_name)

        # db.session.add(category)
        # db.session.commit()
        # return make_response(category.to_dict(), 201)
        
        category = Category(
            category_name=data['category_name']
            )
        
        db.session.add(category)
        db.session.commit()
        return make_response(category.to_dict(), 201)

api.add_resource(Categories, '/categories')

class CategoriesByID(Resource):
    @jwt_required()
    def get(self, id):
        category = Category.query.get(id)
        if category:
            return make_response(category.to_dict(), 200)
        else:
            return {"error": "Category not found"}, 404

    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can edit categories"}, 403
        
        category = Category.query.get(id)
        if not category:
            return {"error": "Category not found"}, 404

        data = request.get_json()
        category_name = data.get('category_name')
        if not category_name:
            return {"error": "Missing category name"}, 400

        category.category_name = category_name
        db.session.commit()
        return make_response(category.to_dict(), 200)

    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only sellers can delete categories"}, 403
        
        category = Category.query.get(id)
        if not category:
            return {"error": "Category not found"}, 404

        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted successfully"}, 200

api.add_resource(CategoriesByID, '/categories/<int:id>')


class Reviews(Resource):
    @jwt_required()
    def get(self):
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(reviews,200)

    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post reviews"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
    
        reviews = Review(
            rating=data['rating'], 
            description=data['description'],
            buyer_id=data['buyer_id'],
            product_id=data['product_id']
            )
        
        db.session.add(reviews)
        db.session.commit()
        return make_response(reviews.to_dict(), 201)

api.add_resource(Reviews, '/reviews')

class ReviewsByID(Resource):
    @jwt_required()
    def get(self,id):
          reviews = Review.query.filter_by(id=id).first()
          if reviews is None:
             return {"error": "Review not found"}, 404
          response_dict = reviews.to_dict()
          return make_response(response_dict, 200)

    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can edit reviews"}, 403
        
        reviews = Review.query.filter_by(id=id).first()
        if reviews is None:
            return {"error": "Review not found"}, 404
        
        data = request.get_json()
        if all(key in data for key in ['rating', 'description' , ]):
            try:   
                reviews.rating = data['rating']
                reviews.description= data['description']
        
                db.session.commit()
                return make_response(reviews.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400

    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can delete reviews"}, 403
        
        reviews = Review.query.filter_by(id=id).first()
        if reviews is None:
            return {"error": "Review not found"}, 404
        
        reviews = Review.query.get_or_404(id)
        db.session.delete(reviews)
        db.session.commit()
        return make_response({'message': 'Review deleted successfully'})

api.add_resource(ReviewsByID, '/review/<int:id>')


class Wishlists(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can view wishlists"}, 403
        
        wishlists = [wishlist.to_dict() for wishlist in Wishlist.query.all()]
        return make_response(wishlists,200)
    
    @jwt_required()
    def  post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post wishlists"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        wishlist = Wishlist(
            product_id=data['product_id']
        )
        
        db.session.add(wishlist)
        db.session.commit()
        return make_response(wishlist.to_dict(), 201)
        
api.add_resource(Wishlists, '/wishlists')

class WishlistByID(Resource):
    @jwt_required()
    def get(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can view wishlists"}, 403
        
        wishlist = Wishlist.query.filter_by(id=id).first()
        if wishlist is None:
            return {"error": "Store not found"}, 404
        response_dict = wishlist.to_dict()
        return make_response(response_dict, 200)

    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can edit wishlists"}, 403
        
        wishlist = Wishlist.query.filter_by(id=id).first()
        if wishlist is None:
            return {"error": "Wishlist not found"}, 404
        
        data = request.get_json()
        if 'product_id' in data:
            try:
                wishlist.product_id = data['product_id']
                db.session.commit()
                return make_response(wishlist.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400
        
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can delete wishlists"}, 403
        
        wishlist = Wishlist.query.filter_by(id=id).first()
        if wishlist is None:
            return {"error": "Wishlist not found"}, 404
        
        wishlist = Wishlist.query.get_or_404(id)
        db.session.delete(wishlist)
        db.session.commit()
        return make_response({'message': 'Wishlist deleted successfully'})

api.add_resource(WishlistByID,'/wishlists/<int:id>')

# Complaint (get post)
class Complaints(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        if claims['role'] != 'admin' and claims['role'] != 'buyer':
            return {"error": "Only admin and buyers can view complaints"}, 403
        
        complaints = [complaint.to_dict() for complaint in Complaint.query.all()]
        return make_response(complaints, 200)
    
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post complaints"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        complaint = Complaint(
            subject=data['subject'],
            body=data['body'],
            store_id=data['store_id'],
            buyer_id=data['buyer_id']
        )
        
        db.session.add(complaint)
        db.session.commit()
        return make_response(complaint.to_dict(), 201)

api.add_resource(Complaints, '/complaints')

# ComplaintByID (get patch delete)
class ComplaintByID(Resource):
    @jwt_required()
    def get(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'admin' and claims['role'] != 'buyer':
            return {"error": "Only admin and buyers can view complaints"}, 403
        
        complaint = Complaint.query.filter_by(id=id).first()
        if complaint is None:
            return {"error": "Complaint not found"}, 404
        return make_response(complaint.to_dict(), 200)
    
    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer' and claims['role'] != 'admin':
            return {"error": "Only buyers and admin can edit complaints"}, 403
        
        complaint = Complaint.query.filter_by(id=id).first()
        if complaint is None:
            return {"error": "Complaint not found"}, 404
        
        data = request.get_json()
        if all(key in data for key in ['subject', 'body']):
            try:
                complaint.subject = data['subject']
                complaint.body = data['body']
                db.session.commit()
                return make_response(complaint.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400
    
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer' and claims['role'] != 'admin':
            return {"error": "Only buyers and admin can delete complaints"}, 403
        
        complaint = Complaint.query.filter_by(id=id).first()
        if complaint is None:
            return {"error": "Complaint not found"}, 404
        
        complaint = Complaint.query.get_or_404(id)
        db.session.delete(complaint)
        db.session.commit()
        return make_response({'message': 'Complaint deleted successfully'})

api.add_resource(ComplaintByID, '/complaint/<int:id>')

# Cart (get post)
class Carts(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can view the cart"}, 403
        
        carts = [cart.to_dict() for cart in Cart.query.all()]
        return make_response(carts, 200)
    
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post to the cart"}, 403
        
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
        
        cart = Cart(
            product_id=data['product_id']
        )
        
        db.session.add(cart)
        db.session.commit()
        return make_response(cart.to_dict(), 201)

api.add_resource(Carts, '/carts')

# CartByID (get delete)
class CartByID(Resource):
    @jwt_required()
    def get(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can view the cart"}, 403
        
        cart = Cart.query.filter_by(id=id).first()
        if cart is None:
            return {"error": "Cart not found"}, 404
        return make_response(cart.to_dict(), 200)
    
    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can edit the cart"}, 403
        
        cart = Cart.query.filter_by(id=id).first()
        if cart is None:
            return {"error": "Cart not found"}, 404
        
        data = request.get_json()
        if 'product_id' in data:
            try:
                cart.product_id = data['product_id']
                db.session.commit()
                return make_response(cart.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        else:
            return {"errors": ["validation errors"]}, 400
    
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can delete the cart"}, 403
        
        cart = Cart.query.filter_by(id=id).first()
        if cart is None:
            return {"error": "Cart not found"}, 404
        
        cart = Cart.query.get_or_404(id)
        db.session.delete(cart)
        db.session.commit()
        return make_response({'message': 'Cart deleted successfully'})

api.add_resource(CartByID, '/cart/<int:id>')


if __name__ == '__main__':
    with app.app_context():
        create_admin()
    app.run(debug=True, port=5500)