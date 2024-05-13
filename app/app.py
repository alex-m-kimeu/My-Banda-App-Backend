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


migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Restful Routes

# Routes for Products
class Products(Resource):
    def get(self):
        products = [product.to_dict() for product in Product.query.all()]
        return make_response(products, 200)

    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        title = data.get('title')
        description = data.get('description')
        seller_id = data.get('seller_id')
        price = data.get('price')
        quantity = data.get('quantity')
        category_id = data.get('category_id')

        # Validate input data
        if not all([title, description, seller_id, price, quantity, category_id]):
            return {"error": "Missing required fields"}, 400

        seller = User.query.get(seller_id)
        category = Category.query.get(category_id)

        if not seller:
            return {"error": "Seller not found"}, 404

        if not category:
            return {"error": "Category not found"}, 404

        product = Product(
            title=title,
            description=description,
            seller_id=seller_id,
            price=price,
            quantity=quantity,
            category_id=category_id
        )

        db.session.add(product)
        db.session.commit()
        return make_response(product.to_dict(), 201)


api.add_resource(Products, '/products')

class ProductsByID(Resource):
    def get(self, id):
        product = Product.query.get(id)
        if product:
            return make_response(product.to_dict(), 200)
        else:
            return {"error": "Product not found"}, 404

    def patch(self, id):
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        data = request.get_json()

        # Validate input data
        if not data:
            return {"error": "Missing data in request"}, 400

        valid_fields = ['title', 'description', 'seller_id', 'price', 'quantity', 'category_id']
        if not all(field in data for field in valid_fields):
            return {"error": "Missing or invalid fields in request"}, 400

        seller = User.query.get(data.get('seller_id'))
        category = Category.query.get(data.get('category_id'))

        if not seller:
            return {"error": "Seller not found"}, 404

        if not category:
            return {"error": "Category not found"}, 404

        product.title = data.get('title')
        product.description = data.get('description')
        product.seller_id = data.get('seller_id')
        product.price = data.get('price')
        product.quantity = data.get('quantity')
        product.category_id = data.get('category_id')

        db.session.commit()
        return make_response(product.to_dict(), 200)

    def delete(self, id):
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200


api.add_resource(ProductsByID, '/products/<int:id>')

#Route for Categories
class Categories(Resource):
    def get(self):
        categories = [category.to_dict() for category in Category.query.all()]
        return make_response(categories, 200)

    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing data in request"}, 400

        category_name = data.get('category_name')
        if not category_name:
            return {"error": "Missing category name"}, 400

        category = Category(category_name=category_name)

        db.session.add(category)
        db.session.commit()
        return make_response(category.to_dict(), 201)


api.add_resource(Categories, '/categories')

class CategoriesByID(Resource):
    def get(self, id):
        category = Category.query.get(id)
        if category:
            return make_response(category.to_dict(), 200)
        else:
            return {"error": "Category not found"}, 404

    def patch(self, id):
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

    def delete(self, id):
        category = Category.query.get(id)
        if not category:
            return {"error": "Category not found"}, 404

        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted successfully"}, 200


api.add_resource(CategoriesByID, '/categories/<int:id>')




if __name__ == '__main__':
    app.run(debug=True, port=5500)