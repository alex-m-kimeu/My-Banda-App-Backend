from flask_bcrypt import Bcrypt
from app import app
from models import db, User, Store,Category, Product, Cart_Product, Cart, Wishlist, Wishlist_Product
from sqlalchemy import text

bcrypt = Bcrypt(app)

def execute_sql(sql):
    """Execute raw SQL."""
    with db.engine.begin() as connection:
        connection.execute(text(sql))


if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        User.query.delete()
        Store.query.delete()
        Category.query.delete()
        Product.query.delete()
        Cart.query.delete()
        Cart_Product.query.delete()
        Wishlist.query.delete()
        Wishlist_Product.query.delete()
           
        print("Seeding users...")
        users = [
            User(username="Peter Mwongela", email="peter@gmail.com", password=bcrypt.generate_password_hash("Peter.123").decode('utf-8'), role='seller', image='https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0712345678"),
            User(username="Candy Bosibori", email="bosibori@gmail.com", password=bcrypt.generate_password_hash("Bosibori.123").decode('utf-8'), role='buyer', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', contact="8798765432"),
            User(username="Alex Kimeu", email="alexkimeu@gmail.com", password=bcrypt.generate_password_hash("AlexKimeu.123").decode('utf-8'), role='buyer', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', contact="4578865323467"),
        ]
        
        store= [
            Store(store_name = "jade collection", description ="fancy clothes everwhaer and anywhere", image="https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600", location="Nairobi west", seller_id=1)
        ]

        category= [
            Category( category_name= 'Clothing')
        ]
         
        products =[
            Product(title="sports shoes", description="lorem impsum nnnn nnn nnn nnn", price= 300.00, quantity=44, images= 'https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', store_id=1, category_id=1),
            Product(title="tutle necks", description="hdck cdwqcg cwacg ckasdycg bcaujcgy", price= 876.00, quantity=55, images= 'https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', store_id=1, category_id=1)
        ] 

        carts=[
            Cart(buyer_id=2),
            Cart(buyer_id=3)
        ]


        cart_products=[
             Cart_Product(product_id=1, cart_id=1),
             Cart_Product(product_id=2, cart_id=1),
             Cart_Product(product_id=1, cart_id=2),
             Cart_Product(product_id=1, cart_id=1)
        ]

        wishlists =[
            Wishlist(buyer_id=2),
            Wishlist(buyer_id=3)
        ]

        wishlist_products=[
             Wishlist_Product(product_id=1, wishlist_id=1),
             Wishlist_Product(product_id=2, wishlist_id=1),
             Wishlist_Product(product_id=1, wishlist_id=2)
        ]

        

        db.session.add_all(users)
        db.session.add_all(store)
        db.session.add_all(category)
        db.session.add_all(products)
        db.session.add_all(carts)
        db.session.add_all(cart_products)
        db.session.add_all(wishlists)
        db.session.add_all(wishlist_products)

        db.session.commit()    
        print("Done seeding!")