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


class ReviewResource(Resource):
    def get(self, review_id):
        review = Review.query.get(review_id)
        return jsonify(review.to_dict())
    
    def post(self):
        data = request.json
        new_review = Review(
            rating=data.get('rating'),
            description=data.get('description'),
            timestamp=data.get('timestamp'),
            buyer_id=data.get('buyer_id'),
            product_id=data.get('product_id')
        )

        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.to_dict()), 201
    
    def put(self, review_id):
        review = Review.query.get_or_404(review_id)
        data = request.json
        review.rating = data.get('rating')
        review.description = data.get('description')
        review.timestamp = data.get('timestamp')
        review.buyer_id = data.get('buyer_id')
        review.product_id = data.get('product_id')
        db.session.commit()
        return jsonify(review.to_dict())
    
    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return jsonify({'message': 'Review deleted successfully'})
    
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')

class WishlistResource(Resource):
    def get(self, wishlist_id):
        wishlist = Wishlist.query.get(wishlist_id)
        if wishlist:
            return jsonify(wishlist.to_dict())
        else:
            return jsonify({'message':'Wishlist not found'}), 404
        
    def post(self):
        data =  request.json
        new_wishlist = Wishlist(
            product_id=data.get('product_id')
        )

        db.session.add(new_wishlist)
        db.session.commit()
        return jsonify(new_wishlist.to_dict()), 201
    
    def put(self, wishlist_id):
        wishlist = Wishlist.query.get_or_404(wishlist_id)
        data = request.json
        wishlist.product_id = data.get('product_id')


        db.session.commit()
        return jsonify(wishlist.to_dict())
    
    def delete(self, wishlist_id):
        wishlist = Wishlist.query.get_or_404(wishlist_id)
        
        db.session.delete(wishlist)
        db.session.commit()
        return jsonify({'message': 'Wishlist deleted successfully'})
    
api.add_resource(WishlistResource, '/wishlist', '/wishlists/<int:wishlist_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5500)