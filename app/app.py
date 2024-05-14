from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os

from models import db, User, Store , Complaint, Cart, Review, Wishlist, Product, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Restful Routes
# USERS (get post)
class Users(Resource):
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
            password=hashed_password,
            contact=data['contact'],
            image=data['image']
            )
        
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 201)


api.add_resource(Users, '/users')

# USERBYID (get patch delete)
class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {"error": "User not found"}, 404
        response_dict = user.to_dict()
        return make_response(response_dict, 200)
    

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


    def delete(self, id):        
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
    def get(self):
        stores = [store.to_dict() for store in Store.query.all()]
        return make_response(stores,200)
        
    
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400
    
        store = Store(
            store_name=data['store_name'], 
            description=data['description'],
            image=data['image'],
            location=data['location']
            )
        
        db.session.add(store)
        db.session.commit()
        return make_response(store.to_dict(), 201)


api.add_resource(Stores, '/stores')

# USERBYID (get patch delete)
class StoreByID(Resource):
    def get(self,id):
        store = Store.query.filter_by(id=id).first()
        if store is None:
            return {"error": "Store not found"}, 404
        response_dict = store.to_dict()
        return make_response(response_dict, 200)
    

    def patch(self,id):
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


    def delete(self, id):        
        store = Store.query.filter_by(id=id).first()
        if store is None:
            return {"error": "Store not found"}, 404
        
        store = Store.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()
        return make_response({'message': 'Store deleted successfully'})
    
api.add_resource(StoreByID, '/store/<int:id>')



# Complaint (get post)
class Complaints(Resource):
    def get(self):
        complaints = [complaint.to_dict() for complaint in Complaint.query.all()]
        return make_response(complaints, 200)
    
    def post(self):
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
    def get(self, id):
        complaint = Complaint.query.filter_by(id=id).first()
        if complaint is None:
            return {"error": "Complaint not found"}, 404
        return make_response(complaint.to_dict(), 200)
    
    def patch(self, id):
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
    
    def delete(self, id):
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
    def get(self):
        carts = [cart.to_dict() for cart in Cart.query.all()]
        return make_response(carts, 200)
    
    def post(self):
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
    def get(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if cart is None:
            return {"error": "Cart not found"}, 404
        return make_response(cart.to_dict(), 200)
    
    def patch(self, id):
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
    
    def delete(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if cart is None:
            return {"error": "Cart not found"}, 404
        
        cart = Cart.query.get_or_404(id)
        db.session.delete(cart)
        db.session.commit()
        return make_response({'message': 'Cart deleted successfully'})

api.add_resource(CartByID, '/cart/<int:id>')



if __name__ == '__main__':
    app.run(debug=True, port=5500)