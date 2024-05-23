from flask_bcrypt import Bcrypt
from app import app
from models import db, User, Store, Product,  Cart, Wishlist, DeliveryCompany, Order
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
        Product.query.delete()
        Cart.query.delete()
        Wishlist.query.delete()
        DeliveryCompany.query.delete()
        Order.query.delete()
           
        print("Seeding users...")
        users = [
            User(username="Peter Mwongela", email="peter@gmail.com", password=bcrypt.generate_password_hash("Peter.123").decode('utf-8'), role='seller', image='https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0712345678"),
            User(username="Candy Bosibori", email="bosibori@gmail.com", password=bcrypt.generate_password_hash("Bosibori.123").decode('utf-8'), role='buyer', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', contact="8798765432"),
            User(username="Alex Kimeu", email="alexkimeu@gmail.com", password=bcrypt.generate_password_hash("AlexKimeu.123").decode('utf-8'), role='buyer', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', contact="4578865323467"),
            User(username="Hamdi Adan", email="hamdi@gmail.com", password=bcrypt.generate_password_hash("Hamdi.123").decode('utf-8'), role='deliverer', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', contact="6543467876523"),
            User(username="Louis Odhiambo", email="louis@gmail.com", password=bcrypt.generate_password_hash("Louis.123").decode('utf-8'), role='deliverer', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', contact="09769087687657"),
        ]
        
        store= [
            Store(store_name = "jade collection", description ="fancy clothes everwhaer and anywhere", image="https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600", location="Nairobi west", seller_id=1)
        ]
        
        products =[
            Product(title="sports shoes", description="lorem impsum nnnn nnn nnn nnn", price= 300.00, quantity=44, images= 'https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', store_id=1, category_name ="Clothing"),
            Product(title="tutle necks", description="hdck cdwqcg cwacg ckasdycg bcaujcgy", price= 400.00, quantity=55, images= 'https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', store_id=1, category_name ="Clothing")
        ] 
        deliveryCompanies= [
            DeliveryCompany(name= 'Glovo', location='western avenue', logo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-oTCfJdO8zwDoyHB7j5tktdQq31w6t31GsA&usqp=CAU', description= 'you call we answer', deliverer_id=4),
            DeliveryCompany(name= 'Jumia', location='south C', logo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-oTCfJdO8zwDoyHB7j5tktdQq31w6t31GsA&usqp=CAU', description= 'at the snap of a finger', deliverer_id=5),
        ]

        carts=[
            Cart(quantity=2,buyer_id=2, product_id=1, subtotal=300.00,  items_cost=0 , total_cost=0) ,
            Cart(quantity=1,buyer_id=2, product_id=2 ,subtotal = 400.00,  items_cost=0, total_cost=0),
            Cart(quantity=1,buyer_id=3, product_id=2, subtotal = 876.00,  items_cost=876.00, total_cost=1076)
        ]

        wishlists =[
            Wishlist(buyer_id=2,product_id=1 ),
            Wishlist(buyer_id=2,  product_id=2),
            Wishlist(buyer_id=3,  product_id=1),
            Wishlist(buyer_id=3,  product_id=2),
        ]


        orders = [
            Order(quantity= 2, price = 200.00, status="Pending", buyer_id=2, product_id=1, store_id= 2),
            Order(quantity= 2,price = 200.00, status="Pending", buyer_id=2, product_id=2, store_id= 1),
        ]
      
        

        db.session.add_all(users)
        db.session.add_all(store)
        db.session.add_all(products)
        db.session.add_all(carts)
        db.session.add_all(wishlists)
        db.session.add_all(deliveryCompanies)
        db.session.add_all(orders)

        db.session.commit()    
        print("Done seeding!")