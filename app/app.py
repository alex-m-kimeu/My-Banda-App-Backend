from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

from models import db, User, Store, Complaint, Cart, Review, Wishlist, Product, Cart_Product, Wishlist_Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

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
            password=hashed_password
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

# Refresh Token
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

# Users (get post)
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
            )
        
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 201)
    
api.add_resource(Users, '/users')

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

        if 'username' in request.form:
            user.username = request.form['username']
        if 'email' in request.form:
            user.email = request.form['email']
        if 'password' in request.form:
            user.password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        if 'contact' in request.form:
            user.contact = request.form['contact']

        if 'image' in request.files:
            image = request.files['image']
            user.upload_image(image)

        try:
            db.session.commit()
            return make_response(user.to_dict(), 200)
        except AssertionError:
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

# Products (get post)
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
        category_name = data.get('category_name')

        images = data.get('images')

        product = Product(
            title=title,
            description=description,
            store_id=store_id,
            price=price,
            quantity=quantity,
            category_name=category_name
        )

        product.upload_images(images)

        db.session.add(product)
        db.session.commit()
        return make_response(product.to_dict(), 201)

api.add_resource(Products, '/products')

# Products By ID (get patch delete)
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

        product.title = data.get('title', product.title)
        product.description = data.get('description', product.description)
        product.store_id = data.get('store_id', product.store_id)
        product.price = data.get('price', product.price)
        product.quantity = data.get('quantity', product.quantity)
        product.category_name = data.get('category_name', product.category_name)

        images = data.get('images')
        if images:
            product.images = []
            product.upload_images(images)

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

# Store (get post)
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

        if 'image' not in request.files:
            return {"error": "No image file provided"}, 400

        store = Store(
            store_name=request.form['store_name'], 
            description=request.form['description'],
            location=request.form['location'],
            seller_id=request.form['seller_id']
        )

        image = request.files['image']
        store.upload_image(image)

        db.session.add(store)
        db.session.commit()
        return make_response(store.to_dict(), 201)

api.add_resource(Stores, '/stores')

# Store By ID 
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
    
        if 'store_name' in request.form:
            store.store_name = request.form['store_name']
        if 'description' in request.form:
            store.description= request.form['description']
        if 'location' in request.form:
            store.location = request.form['location']

        if 'image' in request.files:
            image = request.files['image']
            store.upload_image(image)
    
        try:
            db.session.commit()
            return make_response(store.to_dict(), 200)
        except AssertionError:
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

# Reviews (get post)
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

# Reviews By ID (get patch delete)
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

# Wishlist (get post)
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

# Wishlist By ID (get patch delete)
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


class WishlistByBuyerID(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        buyer_id = claims['id']
        wishlist = Wishlist.query.filter_by(buyer_id=buyer_id).first()
        if not wishlist:
            return {"error": "No Wishlist association with this buyer"}, 404
        return jsonify(wishlist.to_dict() ,200 )
    
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post to the cart"}, 403
        
        buyer_id = claims['id']
        wishlist = Wishlist.query.filter_by(buyer_id=buyer_id).first()
        
        data = request.get_json() 
        wishlist_id = data['wishlist_id']
        if wishlist.id == wishlist_id:
            
            if not data:
                return {"error": "Missing data in request"}, 400
            
            new_cart = Wishlist_Product(
                product_id=data['product_id'],
                wishlist_id=data['wishlist_id'],
            )
            
            db.session.add(new_cart)
            db.session.commit()
            return make_response(new_cart.to_dict(), 201)

api.add_resource(WishlistByBuyerID, '/wishlist/buyer')

class ProductWishlistByBuyerID(Resource):
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can delete the cart"}, 403
        
        buyer_id = claims['id']
        cart = Wishlist.query.filter_by(buyer_id=buyer_id).first()
        

        if cart is None:
            return {"error": "Cart not found"}, 404
        
        if cart:
            MyWishlist = Wishlist_Product.query.get_or_404(id)
            db.session.delete(MyWishlist)
            db.session.commit()
            return make_response({'message': 'Wishlist product deleted successfully'})

api.add_resource(ProductWishlistByBuyerID, '/wishlist/product/<int:id>')

# Complaints (get post)
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

# Complaints By ID (get patch delete)
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
        if claims['role'] != 'admin':
            return {"error": "Only admin can edit complaints"}, 403
        
        complaint = Complaint.query.filter_by(id=id).first()
        if complaint is None:
            return {"error": "Complaint not found"}, 404
        
        data = request.get_json()
        if all(key in data for key in ['status']):
            try:
                complaint.status = data['status']
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

# Cart By ID (get patch delete)
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

class CartByBuyerID(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        buyer_id = claims['id']
        cart = Cart.query.filter_by(buyer_id=buyer_id).first()
        if not cart:
            return {"error": "No Cart association with this buyer"}, 404
        return jsonify(cart.to_dict() )
    
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post to the cart"}, 403
        
        buyer_id = claims['id']
        cart = Cart.query.filter_by(buyer_id=buyer_id).first()
        
        data = request.get_json() 
        cart_id = data['cart_id']
        if cart.id == cart_id:
            
            if not data:
                return {"error": "Missing data in request"}, 400
            
            new_cart = Cart_Product(
                product_id=data['product_id'],
                cart_id=data['cart_id'],
            )
            
            db.session.add(new_cart)
            db.session.commit()
            return make_response(new_cart.to_dict(), 201)

api.add_resource(CartByBuyerID, '/cart/buyer')

class ProductCartByBuyerID(Resource):
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can delete the cart"}, 403
        
        buyer_id = claims['id']
        cart = Cart.query.filter_by(buyer_id=buyer_id).first()
        

        if cart is None:
            return {"error": "Cart not found"}, 404
        
        if cart:
            MyCart = Cart_Product.query.get_or_404(id)
            db.session.delete(MyCart)
            db.session.commit()
            return make_response({'message': 'Cart deleted successfully'})
    pass
api.add_resource(ProductCartByBuyerID, '/cart/product/<int:id>')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        create_admin()
    app.run(debug=True, port=5500)