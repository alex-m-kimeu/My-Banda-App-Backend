from flask import Flask, request, make_response, jsonify, flash
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

from models import db, User, Store, Complaint, Cart, Review, Wishlist, Product, DeliveryCompany, Order

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

        title = request.form.get('title')
        description = request.form.get('description')
        store_id = request.form.get('store_id')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        category_name = request.form.get('category_name')

        product = Product(
            title=title,
            description=description,
            store_id=store_id,
            price=price,
            quantity=quantity,
            category_name=category_name
        )

        images = request.files.getlist('images')
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

        title = request.form.get('title', product.title)
        description = request.form.get('description', product.description)
        store_id = request.form.get('store_id', product.store_id)
        price = request.form.get('price', product.price)
        quantity = request.form.get('quantity', product.quantity)
        category_name = request.form.get('category_name', product.category_name)

        product.title = title
        product.description = description
        product.store_id = store_id
        product.price = price
        product.quantity = quantity
        product.category_name = category_name

        images = request.files.getlist('images')
        if images:
            product.images = []
            product.upload_images(images)

        db.session.commit()
        return make_response(product.to_dict(), 200)
    
    @jwt_required()
    def post(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post to the cart"}, 403
        
        current_buyer_id = claims['id']
        product_to_add = Product.query.get(id)
        product_exists = Cart.query.filter_by(product_id=id, buyer_id=current_buyer_id).first()
        print(product_exists)
        cart = Cart.query.filter_by(buyer_id=current_buyer_id).all()
        if not cart:
        
                new_cart_item = Cart(
                
                quantity= 1,
                product_id=product_to_add.id,
                buyer_id = current_buyer_id,
                items_cost= product_to_add.price,
                total_cost= product_to_add.price +200,
                subtotal = product_to_add.price
    
    
            ) 
                db.session.add(new_cart_item)
                db.session.commit()
                print('Item added added to the cart')
    
              
    
                return make_response(new_cart_item.to_dict(),200)
        else :
            if product_exists:
                try:
                    product_exists.quantity = product_exists.quantity +1
                    db.session.commit()

                    print("product exists" )
                    return make_response(product_exists.to_dict(), 200)
                except:
                    print('quantity not updated')

            else:
        
                new_cart_item = Cart(
                
                quantity= 1,
                product_id=product_to_add.id,
                buyer_id = current_buyer_id,
                items_cost= product_to_add.price,
                total_cost= product_to_add.price +200,
                subtotal = product_to_add.price
    
    
            ) 
                db.session.add(new_cart_item)
                db.session.commit()
                print('Item added added to the cart')
    
        
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

class DeleteDecreaseFromCart(Resource):
    @jwt_required()
    def delete(self,id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can delete to the cart"}, 403
        
        current_buyer_id = claims['id']
        product_exists = Cart.query.filter_by(product_id=id, buyer_id=current_buyer_id).first()
        print(product_exists)
        if product_exists:
            db.session.delete(product_exists)
            db.session.commit()
            return {"message": "Product deleted successfully"}, 200

    @jwt_required()
    def post(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post to the cart"}, 403
        buyer_id = claims['id']
        
        
        cart = Cart.query.filter_by(buyer_id=buyer_id).all()
        if not cart:
            return {"error": "No Cart association with this buyer"}, 404
        
        total_subtotal = sum(ct.subtotal for ct in cart)
        for order in cart:
            order.items_cost= total_subtotal
            order.total_cost = total_subtotal +200
        
        current_buyer_id = claims['id']
        item_to_be_decreased= Cart.query.filter_by(product_id=id, buyer_id=current_buyer_id).first()

        item_to_be_decreased.quantity =max(item_to_be_decreased.quantity - 1, 1)
        item_to_be_decreased.subtotal  = item_to_be_decreased.products.price *item_to_be_decreased.quantity


        db.session.commit()
        return make_response(item_to_be_decreased.to_dict(), 200)
        
api.add_resource(DeleteDecreaseFromCart, '/productdec/<int:id>')

class IncreseInCart(Resource):
    @jwt_required()
    def post(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post to the cart"}, 403
      
        buyer_id = claims['id']
        
        current_buyer_id = claims['id']
        item_to_increased= Cart.query.filter_by(product_id=id, buyer_id=current_buyer_id).first()
        
        cart = Cart.query.filter_by(buyer_id=buyer_id).all()
        if not cart:
            return {"error": "No Cart association with this buyer"}, 404
        
        total_subtotal = sum(ct.subtotal for ct in cart)
        for order in cart:
            order.items_cost= total_subtotal
            order.total_cost = total_subtotal +200

        item_to_increased.quantity =item_to_increased.quantity + 1
        item_to_increased.subtotal  = item_to_increased.products.price *item_to_increased.quantity

        db.session.commit()
        return make_response(item_to_increased.to_dict(), 200)

api.add_resource(IncreseInCart, '/productinc/<int:id>')

class DeliveryCompanies(Resource):
    # get all delivery componies
    @jwt_required()
    def get(self):
        companies = [company.to_dict() for company in DeliveryCompany.query.all()]
        return make_response(companies,200)
    

    # create a company/ post to the already existing comp
    @jwt_required()
    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'deliverer':
            return {"error": "Only deliverers can create delivery companies"}, 403

        if 'logo' not in request.files:
            return {"error": "No logo file provided"}, 400

        new_company = DeliveryCompany(
            name=request.form['name'], 
            description=request.form['description'],
            location=request.form['location'],
            deliverer_id=request.form['deliverer_id']
        )

        logo = request.files['logo']
        new_company.upload_image(logo)

        db.session.add(new_company)
        db.session.commit()
        return make_response(new_company.to_dict(), 201)

api.add_resource(DeliveryCompanies, '/companies')


class DeliveryCompaniesByID(Resource):
    
    @jwt_required()
    def get(self,id):
        company = DeliveryCompany.query.filter_by(id=id).first()
        if company is None:
            return {"error": "Delivery Company not found"}, 404
        response_dict = company.to_dict()
        return make_response(response_dict, 200)
    
    @jwt_required()
    def patch(self,id):
        claims = get_jwt_identity()
        if claims['role'] != 'deliverer':
            return {"error": "Only Deliverers can edit a Delivery company information"}, 403
    
        company = DeliveryCompany.query.filter_by(id=id).first()
        if company is None:
            return {"error": "Store not found"}, 404
    
        # data = request.form if request.form else request.get_json()
        if 'name' in request.form:
            company.name = request.form['name']
        if 'description' in request.form:
            company.description= request.form['description']
        if 'location' in request.form:
            company.location = request.form['location']

        if 'logo' in request.files:
            logo = request.files['logo']
            company.upload_image(logo)
    
        try:
            db.session.add(company)
            db.session.commit()
            return make_response(company.to_dict(), 200)
        except AssertionError:
            return {"errors": ["validation errors"]}, 400
        

        
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'deliverer':
            return {"error": "Only Deliverers can remove a Delivery company"}, 403
             
        company = DeliveryCompany.query.filter_by(id=id).first()
        if company is None:
            return {"error": "Delivery Company not found"}, 404
        
        company = DeliveryCompany.query.get_or_404(id)
        db.session.delete(company)
        db.session.commit()
        return make_response({'message': 'Delivery Company deleted successfully'})
 

api.add_resource(DeliveryCompaniesByID, '/company/<int:id>')

class OrdersByDeliverer(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        if claims['role'] != 'deliverer':
            return {"error": "Only a Deliverer can get their orders"}, 403
        
        current_deliverer_id = claims['id']
        company = DeliveryCompany.query.filter_by(deliverer_id =current_deliverer_id).first()
        orders = Order.query.all()
        for order in orders:
            print(order.deliverycompany_id)
            print(company.id)
            print(company)
            if order.deliverycompany_id == company.id:
                print(order.deliverycompany_id)
                print(company.id)
                orders = Order.query.filter_by(deliverycompany_id =company.id).all()
        
                if orders is None:
                    return{"this store has no orders yet"}
        
                else :
                    all_products = [order.to_dict() for order in orders]
                
        
                return make_response(all_products, 200)

            else:
                return {'msg':'this store has no orders yet'}

api.add_resource(OrdersByDeliverer, '/delivererorders')


class OrdersByStore(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        if claims['role'] != 'seller':
            return {"error": "Only Sellers can get their orders"}, 403
        
        current_seller_id = claims['id']
        store = Store.query.filter_by(seller_id=current_seller_id ).first()
        orders = Order.query.filter_by(store_id =store.id).all()

        if orders:
            all_products = [order.to_dict() for order in orders]
        else:
            return{"this store has no orders yet"}

        return make_response(all_products, 200)

api.add_resource(OrdersByStore, '/storeorders')

class AddDeliverer(Resource):
    @jwt_required()
    def patch(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only a buyer can choose a delivery company"}, 403
        
        buyer_id = claims['id']
        deliveryCompany_to_add = DeliveryCompany.query.get(id)
        customer_orders= Order.query.filter_by(buyer_id=buyer_id).all()

        new_orders=[]
        for order in customer_orders:
            print(order.deliverycompany_id)

            order.deliverycompany_id= deliveryCompany_to_add.id
            print(order)
            new_orders.append(order)
            db.session.commit()  

        return make_response([order.to_dict() for order in new_orders], 200)
        

api.add_resource(AddDeliverer, '/deliverer/<int:id>')

class AddLocation(Resource):
    @jwt_required()
    def patch(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only a buyer can add their location"}, 403
        
        buyer_id = claims['id']
        customer_orders= Order.query.filter_by(buyer_id=buyer_id).all()

        new_orders=[]
        for order in customer_orders:
            
            if 'location' in request.form :
                order.location = request.form['location']
                print(order.location)
                print('location added successfully')

                new_orders.append(order)
                db.session.commit()  
    
        return make_response([order.to_dict() for order in new_orders], 200)
        

api.add_resource(AddLocation, '/location')


class Orders(Resource): 
    @jwt_required()
    def get(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can create orders"}, 403
        
        buyer_id = claims['id']
        customer_orders= Order.query.filter_by(buyer_id=buyer_id).all()

        return make_response([order.to_dict() for order in customer_orders], 200)
        

    @jwt_required()

    def post(self):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can create orders"}, 403
        
        buyer_id = claims['id']
        customer_cart= Cart.query.filter_by(buyer_id=buyer_id).all()
        print(customer_cart)
        if customer_cart:
            total = 0
            for item in customer_cart:
                total += item.products.price * item.quantity
            orders= []    
            for item in customer_cart:
                new_order = Order(
                    quantity= item.quantity,
                    price= item.products.price,
                    buyer_id = item.buyer_id,
                    product_id = item.product_id,
                    store_id = item.products.store_id    
                )
                print(item)
                print(new_order)    
                db.session.add(new_order)
                product = Product.query.get(item.product_id)
                product.quantity -= item.quantity    
                db.session.delete(item)
                
                orders.append(new_order)
                db.session.commit()  
            return make_response([order.to_dict() for order in orders], 200)
        else:
            return {"msg":"no items in cart"}
          
api.add_resource(Orders, '/orders')


class OrdersByID(Resource):
    @jwt_required()
    def get(self,id):
        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"error": "Order not found"}, 404
        response_dict = order.to_dict()
        return make_response(response_dict, 200)
    
    @jwt_required()
    def patch(self,id):

        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"error": "Order not found"}, 404
        
        # data = request.form if request.form else request.get_json()
        if 'status' in request.form :
            order.status = request.form['status']
    
            try:
                db.session.commit()
                print("status changed successfully")
                return make_response(order.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
        

    @jwt_required()
    def delete(self, id):
             
        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"error": "Order not found"}, 404
        
        
        if order.status == "Completed" or order.status == "Cancellled":
            order = Order.query.get_or_404(id)
            db.session.delete(order)
            db.session.commit()
            return make_response({'message': 'Order deleted successfully'})
        else :
            return {'msg':'Order hass not yet been fullfilled'}
        
   
api.add_resource(OrdersByID, '/orderByID/<int:id>')

class DeliveryStatus(Resource):
    @jwt_required()
    def get(self,id):
        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"error": "Order not found"}, 404
        response_dict = order.to_dict()
        return make_response(response_dict, 200)
    
    @jwt_required()
    def patch(self,id):

        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"error": "Order not found"}, 404
        
        # data = request.form if request.form else request.get_json()
        if 'delivery_status' in request.form:
            order.delivery_status = request.form['delivery_status']
    
            try:
                db.session.commit()
                print("status changed successfully")
                return make_response(order.to_dict(), 200)
            except AssertionError:
                return {"errors": ["validation errors"]}, 400
            
    @jwt_required()
    def delete(self, id):
             
        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"error": "Order not found"}, 404
        
        
        if order.status == "Completed" or order.status == "Cancellled"or  order.status == "Denied":
            order = Order.query.get_or_404(id)
            db.session.delete(order)
            db.session.commit()
            return make_response({'message': 'Order deleted successfully'})
        else :
            return {'msg':'Order hass not yet been fullfilled'}
    

api.add_resource(DeliveryStatus, '/deliveryorderByID/<int:id>')


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
            return {"error": "Only buyers can view the cart"}, 403
        buyer_id = claims['id']
        wishlists= Wishlist.query.filter_by(buyer_id=buyer_id).all()
        if not wishlists:
            return [], 200
     
        return jsonify([wishlist.to_dict(rules=()) for wishlist in wishlists])
    
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
    def post(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can post to the cart"}, 403
        
        current_buyer_id = claims['id']
        product_to_add = Product.query.get(id)
        product_exists = Wishlist.query.filter_by(product_id=id, buyer_id=current_buyer_id).first()
        if  not product_exists:
        
                new_wishlist_item = Wishlist(
                product_id=product_to_add.id,
                buyer_id = current_buyer_id,
            ) 
                db.session.add(new_wishlist_item)
                db.session.commit()
                print('Item added to the wishlist')
                return make_response(new_wishlist_item.to_dict(),200)
        else :
               return {"message": "Product already exists in the wishlist"}, 200
            
    @jwt_required()
    def delete(self,id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can delete to the cart"}, 403
        
        current_buyer_id = claims['id']
        product_exists = Wishlist.query.filter_by(product_id=id, buyer_id=current_buyer_id).first()
        if product_exists:
            db.session.delete(product_exists)
            db.session.commit()
            return {"message": "Product deleted successfully from the wishlist"}, 200
        
api.add_resource(WishlistByID,'/wishlists/<int:id>')

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
        buyer_id = claims['id']
        cart = Cart.query.filter_by(buyer_id=buyer_id).all()
        if not cart:
            return [], 200
        
        total_subtotal = sum(ct.subtotal for ct in cart)
        for order in cart:
            order.items_cost= total_subtotal
            order.total_cost = total_subtotal +200    

        return jsonify([ct.to_dict(rules=()) for ct in cart])
    
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
            return [], 200
        return make_response(cart.to_dict(), 200)
    
    @jwt_required()
    def delete(self, id):
        claims = get_jwt_identity()
        if claims['role'] != 'buyer':
            return {"error": "Only buyers can delete from the cart"}, 403

        cart_item = Cart.query.filter_by(id=id, buyer_id=claims['id']).first()
        if not cart_item:
            return {"error": "Item not found in cart"}, 404

        db.session.delete(cart_item)
        db.session.commit()
        return {"message": "Item deleted from cart successfully"}, 200

api.add_resource(CartByID, '/cart/<int:id>')


# Run the app
if __name__ == '__main__':
    with app.app_context():
        create_admin()
    app.run(debug=True, port=5500)