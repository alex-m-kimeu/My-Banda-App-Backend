from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os

from models import db, User, Store, Complaint, Cart, Review, Wishlist, Product, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
load_dotenv()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)

migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Hardcode Admin Credentials
def create_admin():
    admin_email = "mybanda.admin@gmail.com"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        hashed_password = bcrypt.generate_password_hash("Admin123!").decode('utf-8')
        admin = User(
            username="Banda Admin", 
            email=admin_email,
            role="admin",
            password=hashed_password,
            contact="1234567890",
            image="https://www.pngegg.com/en/png-ogqel"
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
            password=hashed_password,
            contact=data['contact'],
            image=data['image']
            )
        
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 201)

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


if __name__ == '__main__':
    with app.app_context():
        create_admin()
    app.run(debug=True, port=5500)