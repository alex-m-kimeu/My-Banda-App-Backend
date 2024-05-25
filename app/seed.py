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
           
        print("Seeding Users...")
        users = [
            User(username="My Banda", email="banda.admin@gmail.com", password=bcrypt.generate_password_hash("Admin123!").decode('utf-8'), role='admin', image='https://images.pexels.com/photos/15664597/pexels-photo-15664597/free-photo-of-portrait-of-man.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0700000000"),
            User(username="Peter Mwongela", email="peter@gmail.com", password=bcrypt.generate_password_hash("Peter123!").decode('utf-8'), role='seller', image='https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0700000001"),
            User(username="Candy Bosibori", email="bosibori@gmail.com", password=bcrypt.generate_password_hash("Candy123!").decode('utf-8'), role='buyer', image='https://images.pexels.com/photos/20434992/pexels-photo-20434992/free-photo-of-jasmine-bajwa-model-shoot.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0700000002"),
            User(username="Alex Kimeu", email="alex@gmail.com", password=bcrypt.generate_password_hash("Alex123!").decode('utf-8'), role='seller', image='https://images.pexels.com/photos/1121796/pexels-photo-1121796.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0700000003"),
            User(username="Hamdi Adan", email="hamdi@gmail.com", password=bcrypt.generate_password_hash("Hamdi123!").decode('utf-8'), role='deliverer', image='https://images.pexels.com/photos/8067738/pexels-photo-8067738.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0700000004"),
            User(username="Louis Odhiambo", email="louis@gmail.com", password=bcrypt.generate_password_hash("Louis123!").decode('utf-8'), role='deliverer', image='https://images.pexels.com/photos/1680172/pexels-photo-1680172.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0700000005"),
            User(username="Eric Kimeu", email="eric@gmail.com", password=bcrypt.generate_password_hash("Eric123!").decode('utf-8'), role='seller', image='https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0700000006"),
        ]
        
        print("Seeding Stores...")
        store= [
            Store(store_name = "Glitz & Glamour", description ="Discover your unique style at Glitz & Glamour, where fashion meets affordability. From trendy outfits to timeless classics, we have got everything you need to look and feel your best. Step into style today!", image="https://images.unsplash.com/photo-1579108189501-b3af293abbf8?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGNsb3RoaW5nJTIwc2hvcHxlbnwwfHwwfHx8MA%3D%3D", location="Nairobi, Kenya", seller_id=2),
            Store(store_name = "Sneaker Haven", description ="Welcome to Sneaker Haven! Where style meets sole! Discover the latest releases, exclusive drops, and classic kicks from top brands like Nike, Adidas, and Jordan. Our passionate team is here to help you find your perfect pair. Step into Sneaker Haven and elevate your sneaker game today!", image="https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fHNuZWFrZXIlMjBzaG9wfGVufDB8fDB8fHww", location="Kilimani, Nairobi", seller_id=4),
            Store(store_name = "Trendy Threads", description ="Welcome to Trendy Threads! We are your one-stop shop for the latest fashion trends. Our curated collection of clothing and accessories is designed to help you express your unique style. Whether you're looking for casual basics or statement pieces, we've got you covered. Shop now and discover your new favorite look!", image="https://images.pexels.com/photos/12026051/pexels-photo-12026051.jpeg?auto=compress&cs=tinysrgb&w=600", location="Nakuru, Kenya", seller_id=7),
        ]
        
        print("Seeding Products...")
        products =[
            Product(title="Navy Cord Shirt-Jacket", description="Made for him or her, this shirt-jacket is perfect for those in-between days when you need an extra layer but don't want to compromise on style. Pair them with your favourite jeans and a t-shirt for a relaxed and casual look, or dress them up with chinos and a shirt for a more refined ensemble.", price= 160.00, quantity=40, images= ['https://koyclothing.com/cdn/shop/files/CordShacket_1024x1024.jpg?v=1709547242', 'https://koyclothing.com/cdn/shop/files/Bestseller1_2_6337911e-d165-40d5-8665-ba4155a97656_640x.png?v=1709547242', 'https://koyclothing.com/cdn/shop/files/NavyShacket5_640x.png?v=1709547242', 'https://koyclothing.com/cdn/shop/files/NavyShacket3_640x.png?v=1709547242'], store_id=1, category_name ="Clothing"),
            
            Product(title="Chukka Push Shoe", description="A non-Sidestripe style that honors our heritage while pushing the boundaries of style forward, the Chukka Push utilizes exaggerated Y2K and skate-inspired flare on a classic blucher toe. Simple but exaggerated, this modernized 90s style expands on the nostalgia trend while blazing its own forward-looking trail.", price= 60.00, quantity=40, images= ['https://images.vans.com/is/image/Vans/VN000CZW_JVY_HERO?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CZW_JVY_ALT1?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CZW_JVY_ALT2?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CZW_JVY_ALT3?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0'], store_id=2, category_name ="Shoes"),
            
            Product(title="Mary Jane Shoe", description="Tapping into retro nostalgia and a playful interpretation of femininity, the Vans Mary Jane takes this timeless silhouette and cranks it up a notch. Pairing a simple buckle and strap with a rubber toe cap, stark black upper, and our signature rubber waffle outsole, the Mary Jane delivers the perfect blend of casual and classy, ideal for . . . well, just about anything.", price= 120.00, quantity=30, images= ['https://images.vans.com/is/image/Vans/VN000CRR_BJ4_HERO?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CRR_BJ4_ALT1?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CRR_BJ4_ALT2?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CRR_BJ4_ALT3?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0'], store_id=2, category_name ="Shoes"),
            
            Product(title="Old Skool Shoe", description="The Color Theory Collection allows you to create a unique color story by pairing vibrant, unexpected hues with our iconic footwear styles. Made with a classic pairing of canvas and suede, this Old Skool honors our heritage Sidestripe silhouette while offering a fresh look that boosts the appeal of this unmistakable shoe.", price= 80.00, quantity=20, images= ['https://images.vans.com/is/image/Vans/VN000CT8_CIB_HERO?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CT8_CIB_ALT1?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CT8_CIB_ALT2?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0', 'https://images.vans.com/is/image/Vans/VN000CT8_CIB_ALT3?wid=1600&hei=1984&fmt=jpeg&qlt=90&resMode=sharp2&op_usm=0.9,1.7,8,0'], store_id=2, category_name ="Shoes"),
            
            Product(title="Nike Dunk Low", description="Created for the hardwood but taken to the streets, this 80s basketball icon returns with classic details and throwback hoops flair. Synthetic leather overlays help the Nike Dunk channel vintage style while its padded, low-cut collar lets you take your game anywhere—in comfort.", price= 115.00, quantity=10, images= ['https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/338d0737-bd55-4b33-86f4-e2f92a11d3c8/dunk-low-mens-shoes-l12Bc1.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/8f03587f-3fcd-4825-98b0-cc3d76f6c486/dunk-low-mens-shoes-l12Bc1.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/e16bbc69-5566-485b-925f-0c6e8d243eaf/dunk-low-mens-shoes-l12Bc1.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b2257c24-2bea-49c7-a934-f820f60a5221/dunk-low-mens-shoes-l12Bc1.png'], store_id=2, category_name ="Shoes"),
            
            Product(title="Kamba Navy Linen Shirt", description="Made from 100% pure linen in a striking navy-blue colour with eye-catching Kenyan Kikoy Fabric detailing on the inner collar stand, hem gusset, cuffs and sleeve plackets.", price= 100.00, quantity=30, images= ['https://koyclothing.com/cdn/shop/products/NavyLinen_640x.jpg?v=1710923196', 'https://koyclothing.com/cdn/shop/products/BlueCord1_3_868108d1-a6c1-4df1-9ea2-6401a42d371d_640x.png?v=1697537126', 'https://koyclothing.com/cdn/shop/products/BlueCord1_4_91f661e2-b7c1-4b6d-97d0-5507278d6839_640x.png?v=1697537126', 'https://koyclothing.com/cdn/shop/products/BlueCord1_2_cca7634d-4183-42aa-b32e-1f59312ea926_640x.png?v=1697537126'], store_id=1, category_name ="Clothing"),
            
            Product(title="Nike Dunk Low Retro", description="Created for the hardwood but taken to the streets, the basketball icon returns with classic details and throwback hoops flair. Channeling '80s vibes, its padded, low-cut collar lets you take your game anywhere—in comfort.", price= 90.00, quantity=15, images= ['https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/4f2fd75c-10f4-4249-a4f7-b38d57646f8f/dunk-low-retro-mens-shoes-76KnBL.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/4ea08d04-7eee-4d62-8a95-39f85f7be223/dunk-low-retro-mens-shoes-76KnBL.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/a60c0e51-7cc7-40f9-9860-942f809dfff3/dunk-low-retro-mens-shoes-76KnBL.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/a788613c-1644-4c84-a090-66c79bb9abf3/dunk-low-retro-mens-shoes-76KnBL.png'], store_id=2, category_name ="Shoes"),
            
            Product(title="Pink Linen Blend Blazer", description="Made from 100% pure linen in a striking navy-blue colour with eye-catching Kenyan Kikoy Fabric detailing on the inner collar stand, hem gusset, cuffs and sleeve plackets.", price= 350.00, quantity=25, images= ['https://koyclothing.com/cdn/shop/files/PinkLinenBlazer_640x.jpg?v=1709294525', 'https://koyclothing.com/cdn/shop/files/PinkLinenBlazer_7_640x.jpg?v=1709294525', 'https://koyclothing.com/cdn/shop/files/PinkLinenBlazer_8_640x.jpg?v=1709294525', 'https://koyclothing.com/cdn/shop/files/PinkLinenBlazer_6_640x.jpg?v=1709294525'], store_id=1, category_name ="Clothing"),
            
            Product(title="Air Jordan 1 Mid", description="Inspired by the original AJ1, the Air Jordan 1 Mid offers fans a chance to follow in MJ's footsteps. Fresh color trims the clean, classic materials, imbuing modernity into a classic design.", price= 120.00, quantity=25, images= ['https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/i1-12a6b727-3f70-4838-b4dd-de81f6a64baa/air-jordan-1-mid-shoes-X5pM09.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/i1-be7631d2-9c26-4d0d-8626-9aa1d2101e00/air-jordan-1-mid-shoes-X5pM09.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/i1-bb85e220-1e4d-479c-ac5b-80019057fcc3/air-jordan-1-mid-shoes-X5pM09.png', 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/i1-a1cf4e50-cfa4-4cf1-a13d-4bd377e2f63e/air-jordan-1-mid-shoes-X5pM09.png'], store_id=2, category_name ="Shoes"),
            
            Product(title="Mida Blue Linen Shirt", description="Made with a luxurious blend linen and cotton materials. The combination of cotton and linen keeps the lightweight and breathable nature of a linen shirt, yet adds the softness of cotton. Named after the clear blue waters of 'Mida Creek' in Watamu, Kenya. Reflecting the quality of the creek's waters, and accompanied beautifully with an African sunset.", price= 120.00, quantity=20, images= ['https://koyclothing.com/cdn/shop/files/MidaBlueJimmy1_1024x1024.jpg?v=1708696877', 'https://koyclothing.com/cdn/shop/files/5061037530040_3_640x.jpg?v=1708944950', 'https://koyclothing.com/cdn/shop/files/MidaBlue_5_640x.jpg?v=1708944950', 'https://koyclothing.com/cdn/shop/files/MidaBlue_4_640x.jpg?v=1708944950'], store_id=1, category_name ="Clothing"),
            
            Product(title="Ranger Jacket", description="The ultimate fusion of rugged outdoor styling and timeless elegance. Crafted from a luxurious blend of cotton and linen materials, this beige bomber jacket is the perfect addition to your wardrobe for any outdoor adventure or casual outing. Customary with our designs, the unique blue and white mottled Kenyan Kikoy fabric is expertly hand-sewn on the inside of the jacket, adding a unique flash of African-inspired colour.", price= 140.00, quantity=60, images= ['https://koyclothing.com/cdn/shop/products/Ranger3_640x.png?v=1681226277', 'https://koyclothing.com/cdn/shop/products/Ranger4_640x.png?v=1681226277', 'https://koyclothing.com/cdn/shop/products/BlueCord1_44_640x.png?v=1683639478', 'https://koyclothing.com/cdn/shop/files/Rangerghost_640x.png?v=1683639478'], store_id=1, category_name ="Clothing"),
            
            
        ]
        
        print("Seeding Delivery Companies...")
        deliveryCompanies= [
            DeliveryCompany(name= 'Glovo', location='western avenue', logo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbNUfKcHKZAVLlAQxa2P4u9-gZ57V3ceAT6qDaZL4bNQ&s', description= 'Lightning-Fast Deliveries, Right to Your Doorstep! We pride ourselves on speed and reliability, ensuring your packages arrive in record time, every time."', deliverer_id=5),
            DeliveryCompany(name= 'Uber', location='south C', logo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgPceKxW5qSEzYBZsEdjpzQC8QDZI7EnYpiUoYC3TygHaDqDAGIF8UTd5QxY5Hr_acQaY&usqp=CAU', description= ' Your Fast Track to Reliable Delivery. Experience the future of shipping with our ultra-efficient, same-day delivery service that keeps you moving forward."', deliverer_id=6),
        ]

        db.session.add_all(users)
        db.session.add_all(store)
        db.session.add_all(products)
        db.session.add_all(deliveryCompanies)

        db.session.commit()    
        print("Done seeding!")