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
            User(username="John Doe", email="john@gmail.com", password=bcrypt.generate_password_hash("John123!").decode('utf-8'), role='seller', image='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fHByb2ZpbGUlMjBwaWN1cmV8ZW58MHx8MHx8fDA%3D', contact="0700000007"),
            User(username="Jane Doe", email="jane@gmail.com", password=bcrypt.generate_password_hash("Jane123!").decode('utf-8'), role='seller', image='https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8cHJvZmlsZSUyMHBpY3R1cmV8ZW58MHx8MHx8fDA%3D', contact="0700000008"),
            User(username="Peter Parker", email="parker@gmail.com", password=bcrypt.generate_password_hash("Parker123!").decode('utf-8'), role='seller', image='https://images.unsplash.com/photo-1601233749202-95d04d5b3c00?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8bWFsZSUyMHByb2ZpbGUlMjBwaWN0dXJlfGVufDB8fDB8fHww', contact="0700000009"),
        ]
        
        print("Seeding Stores...")
        store= [
            Store(store_name = "Glitz & Glamour", description ="Discover your unique style at Glitz & Glamour, where fashion meets affordability. From trendy outfits to timeless classics, we have got everything you need to look and feel your best. Step into style today!", image="https://images.unsplash.com/photo-1579108189501-b3af293abbf8?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGNsb3RoaW5nJTIwc2hvcHxlbnwwfHwwfHx8MA%3D%3D", location="Nairobi, Kenya", seller_id=2),
            Store(store_name = "Sneaker Haven", description ="Welcome to Sneaker Haven! Where style meets sole! Discover the latest releases, exclusive drops, and classic kicks from top brands like Nike, Adidas, and Jordan. Our passionate team is here to help you find your perfect pair. Step into Sneaker Haven and elevate your sneaker game today!", image="https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fHNuZWFrZXIlMjBzaG9wfGVufDB8fDB8fHww", location="Kilimani, Nairobi", seller_id=4),
            Store(store_name = "Trendy Threads", description ="Welcome to Trendy Threads! We are your one-stop shop for the latest fashion trends. Our curated collection of clothing and accessories is designed to help you express your unique style. Whether you're looking for casual basics or statement pieces, we've got you covered. Shop now and discover your new favorite look!", image="https://images.pexels.com/photos/12026051/pexels-photo-12026051.jpeg?auto=compress&cs=tinysrgb&w=600", location="Nakuru, Kenya", seller_id=7),
            Store(
                store_name="Gleaming Gems",
                description="Welcome to Gleaming Gems! We are your premier destination for exquisite jewelry. Our curated collection of fine jewelry and accessories is designed to help you shine on any occasion. Whether you're looking for timeless classics or contemporary designs, we've got you covered. Shop now and discover your new favorite piece of jewelry!",
                image="https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8amV3ZWxsZXJ5fGVufDB8fDB8fHww",
                location="Nakuru, Kenya",
                seller_id=8
            ),
            Store(
                store_name="Vitality Hub",
                description="Welcome to Vitality Hub! We are your ultimate destination for health and fitness essentials. Our curated collection of fitness equipment, supplements, and activewear is designed to help you achieve your wellness goals. Whether you're a seasoned athlete or just starting your fitness journey, we've got everything you need. Shop now and take the first step towards a healthier, stronger you!",
                image="https://images.unsplash.com/photo-1627483298606-cf54c61779a9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxzZWFyY2h8MXx8Zml0bmVzc3xlbnwwfHwwfHx8MA%3D%3D",
                location="Nakuru, Kenya",
                seller_id=9
            ),
            Store(
                store_name="TechZone",
                description="Welcome to TechZone! We're your go-to destination for the latest electronics and gadgets. Explore our curated collection of smartphones, laptops, smart home devices, and more. Whether you're a tech enthusiast or just looking for the latest innovations, we've got you covered. Shop now and stay ahead with the cutting-edge technology!",
                image="https://images.unsplash.com/photo-1571857089849-f6390447191a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8ZWxlY3Ryb25pY3MlMjBzdG9yZXxlbnwwfHwwfHx8MA%3D%3D",
                location="San Francisco, USA",
                seller_id=10
            )
        

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
            
            


            Product(
                title="Eternal Elegance Necklace",
                description="A stunning symbol of everlasting beauty, the Eternal Elegance Necklace features a sparkling diamond pendant set in 18k white gold. The delicate chain is designed to lay gracefully against your skin, making it the perfect accessory for any occasion. Elevate your elegance with this timeless piece.",
                price=520.00,
                quantity=30,
                images=[
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/24024/original/3_White_Topaz_Round_Necklace_FlatLay.jpg?1646761076',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/24023/original/2_Mejuri_MarchDrops__26_White_Topaz_Round_Necklace_Stack_3359.jpg?1646761066',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/24022/original/1_Mejuri_MarchDropsv_White_Topaz_Round_Necklace_Solo_4712.jpg?1646761054',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/24021/original/0_White_Topaz_Round_Necklace_Front.jpg?1646761043',
                ],
                store_id=4,
                category_name="Jewelry"
            ),
            Product(
                title="Radiant Rose Gold Bracelet",
                description="Adorn your wrist with the Radiant Rose Gold Bracelet, a chic and modern piece crafted from high-quality rose gold. Its minimalist design and subtle shine make it versatile enough for both casual and formal wear. A true testament to refined craftsmanship.",
                price=320.00,
                quantity=50,
                images=[
                    'https://shopsoko.com/cdn/shop/products/DashCuffBracelet-gold.jpg?crop=center&height=1200&v=1674503597&width=800',
                    'https://shopsoko.com/cdn/shop/products/Soko-Sept-Campaign-Thomas-Welch-163_1.jpg?v=1674503597',
                    'https://shopsoko.com/cdn/shop/products/DashCuffBracelet.jpg?v=1674503597',
                    'https://shopsoko.com/cdn/shop/products/Soko-Sept-Campaign-Thomas-Welch-145_3_1.jpg?v=1674503597',
                ],
                store_id=4,
                category_name="Jewelry"
            ),
            Product(
            title="Twilight Sapphire Earrings",
            description="Glimmering with the deep hues of twilight, these Sapphire Earrings are crafted to perfection. Set in sterling silver, the sapphires are beautifully complemented by delicate diamond accents. These earrings add a touch of sophistication to any outfit.",
            price=450.00,
            quantity=40,
            images=[
                'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/17007/original/OrganicPearlHoops_earrings_v_hero_1240.jpg?1605794379',
                'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/6503/original/Feb_7__2019_-_Studio_Session_-_Carina-019-Feb_07_2019.jpg?1550070243',
                'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/18507/original/OrganicPearlHoops_earrings_v_alt_1419.jpg?1606418090',
                'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/17007/original/OrganicPearlHoops_earrings_v_hero_1240.jpg?1605794379',
            ],
            store_id=4,
            category_name="Jewelry"
        ),
        Product(
                title="Celestial Charm Braclet",
                description="Step out in style with the Celestial Charm Braclet. This delicate piece is adorned with star and moon charms, crafted from high-quality sterling silver. Perfect for adding a whimsical touch to your summer outfits or beachwear.",
                price=120.00,
                quantity=75,
                images=[
                    'https://shopsoko.com/cdn/shop/products/SOKO-amali-stacking-cuffs-gold-1.png?crop=center&height=975&v=1716513997&width=650',
                    'https://shopsoko.com/cdn/shop/products/SOKO-model-wearing-Amali-Stacking-Cuffs-Gold-2.png?v=1664985518',
                    'https://shopsoko.com/cdn/shop/products/SOKO-model-wearing-Amali-Stacking-Cuffs-Gold-1.png?v=1664985518',
                    'https://shopsoko.com/cdn/shop/products/SOKO-amali-stacking-cuffs-silver-1.png?v=1664985518'
                ],
                store_id=4,
                category_name="Jewelry"
            ),
            Product(
                title="Vintage Opal Ring",
                description="Discover the magic of the Vintage Opal Ring, featuring a radiant opal set in antique gold. The intricate detailing around the band highlights the opal's natural beauty, making this ring a standout addition to any jewelry collection.",
                price=380.00,
                quantity=20,
                images=[
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/24041/original/0_Round_Cut_Topaz_Studs.jpg?1646762499',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/24043/original/2_Round_Cut_Topaz_Studs.jpg?1646762520',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/24044/original/4_Round_Cut_Topaz_Studs.jpg?1646762531',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/24045/original/Butterfly_EarringBackings.jpg?1646762545',
                ],
                store_id=4,
                category_name="Jewelry"
            ),
            Product(
                title="Luminous Pearl Choker",
                description="Embrace elegance with the Luminous Pearl Choker. Featuring a single strand of perfectly round pearls, this choker sits gracefully around your neck. It's an ideal piece for weddings, parties, or any special event where you want to shine.",
                price=300.00,
                quantity=35,
                images=[
                    'https://shopsoko.com/cdn/shop/products/Kazuri_Pearl_Choker_Cornflower.jpg?v=1649272471',
                    'https://shopsoko.com/cdn/shop/products/MpiraBoneChokerNecklace_Blue.jpg?v=1649272471',
                    'https://shopsoko.com/cdn/shop/products/Kazuri_Pearl_Choker_Fawn.jpg?v=1649272471',
                    'https://shopsoko.com/cdn/shop/products/MpiraBoneChokerNecklace_Nude.jpg?v=1649272471',
                ],
                store_id=4,
                category_name="Jewelry"
            ),
           Product(
                title="Majestic Amethyst Ring",
                description="The Majestic Amethyst Ring is a true masterpiece, featuring a vibrant amethyst gemstone set in a meticulously crafted sterling silver band. The gemstone's deep purple hue is enhanced by the surrounding intricate detailing, making it a regal addition to any jewelry collection. Perfect for adding a touch of luxury to both everyday and formal wear.",
                price=340.00,
                quantity=50,
                images=[
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/30892/original/0-HeartSignet-14K-Angled_022.jpg?1699368476',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/30894/original/3-HeartSignet-14K-Back_456.jpg?1699368500',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/30893/original/1-HeartSignet14k-14k-Solo_042.jpg?1699368487',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/30895/original/4-HeartSignet-14K-Engraved_367.jpg?1699368511',
                ],
                store_id=4,
                category_name="Jewelry"
            ),
            Product(
                title="Heirloom Ruby Pendant",
                description="The Heirloom Ruby Pendant is a timeless piece that exudes elegance and sophistication. Featuring a deep red ruby set in 14k gold, this pendant is perfect for adding a pop of color to your wardrobe. Ideal for both everyday wear and special occasions.",
                price=600.00,
                quantity=15,
                images=[
                    'https://shopsoko.com/cdn/shop/files/IMG_9636.jpg?v=1706817628',
                    'https://shopsoko.com/cdn/shop/files/IMG_0540.jpg?v=1707264078',
                    'https://shopsoko.com/cdn/shop/files/IMG_9999.jpg?v=1707266764',
                    'https://shopsoko.com/cdn/shop/files/SO230106354320_green.jpg?v=1707266764',
                
                ],
                store_id=4,
                category_name="Jewelry"
            ),
            Product(
                title="Mystic Topaz Ring",
                description="The Mystic Topaz Ring showcases a mesmerizing topaz gemstone that changes colors in different lights. Set in sterling silver with delicate detailing, this ring is a true statement piece that will captivate everyone's attention.",
                price=280.00,
                quantity=45,
                images=[
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/30423/original/0-DiamondPearlStackerRing-14k-Angled_597.jpg?1696640110',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/30424/original/1-DiamondPearlStackerRing-14K-Stack2_019.jpg?1696640132',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/30426/original/3-DiamondPearlStackerRing-14k-Front_365.jpg?1696640170',
                    'https://static.mejuri.com/mejuri-com/image/fetch/c_scale,f_auto,q_60,w_1500/https://static.mejuri.com/legacy-front/production/system/spree/products/30427/original/4-DiamondPearlStackerRing-14k-MacroDetail_806.jpg?1696640189',
                ],
                store_id=4,
                category_name="Jewelry"
            ),
            Product(
                title="Golden Leaf Earrings",
                description="Inspired by nature, the Golden Leaf Earrings feature intricate leaf designs crafted from 18k gold. These earrings are lightweight and versatile, making them the perfect accessory for any outfit, from casual to formal.",
                price=190.00,
                quantity=60,
                images=[
                    'https://shopsoko.com/cdn/shop/products/JuaCapsuleHoop.jpg?v=1641416253',
                    'https://shopsoko.com/cdn/shop/products/JuaCapsuleHoopEarring_2.jpg?v=1649868768',
                    'https://shopsoko.com/cdn/shop/products/JuaCapsuleHoop_53c2d4ee-edb0-4919-b0a0-178f81299b10.jpg?v=1649868768',
                    'https://shopsoko.com/cdn/shop/products/JuaCapsuleHoopEarring_1.jpg?v=1649868768',
                ],
                store_id=4,
                category_name="Jewelry"
            ),




             Product(
                title="Radiant Glow Face Serum",
                description="Achieve a radiant complexion with the Radiant Glow Face Serum. Packed with powerful antioxidants and vitamins, this serum hydrates, brightens, and revitalizes your skin, giving you a youthful, glowing appearance.",
                price=45.00,
                quantity=100,
                images=[
                    'https://m.media-amazon.com/images/I/618T0f8mylL._SX679_.jpg',
                    'https://m.media-amazon.com/images/I/81uJJEGBpDL._SX679_.jpg',
                    'https://m.media-amazon.com/images/I/61VV4uRFHWL._SX679_.jpg',
                    'https://m.media-amazon.com/images/I/91WVz2tvLIL.jpg',
                ],
                store_id=4,
                category_name="Health & beauty"
            ),
            Product(
    title="SilkySmooth Hair Mask",
    description="Revitalize your hair with the SilkySmooth Hair Mask. This deep conditioning treatment nourishes and repairs damaged hair, leaving it soft, shiny, and manageable. Perfect for all hair types, it restores moisture and strengthens strands.",
    price=25.00,
    quantity=80,
    images=[
        'https://m.media-amazon.com/images/I/41kn8LxFavL._SX300_SY300_QL70_FMwebp_.jpg',
        'https://m.media-amazon.com/images/I/61tIjsp-UWL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/5164kg3nLHL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/61Ajf1jHfQL._SX679_.jpg',
    ],
    store_id=5,
    category_name="Health & beauty"
),
 Product(
    title="Aloe Vera Soothing Gel",
    description="Soothe and hydrate your skin with Aloe Vera Soothing Gel. This multi-purpose gel is perfect for calming sunburn, moisturizing dry skin, and reducing redness. Its natural, gentle formula makes it ideal for all skin types.",
    price=15.00,
    quantity=150,
    images=[
        'https://m.media-amazon.com/images/I/31MkjmugRYL._SX300_SY300_QL70_FMwebp_.jpg',
        'https://m.media-amazon.com/images/I/61ak7mFXENL._SX522_.jpg',
        'https://m.media-amazon.com/images/I/71VVnArETxL._SX522_.jpg',
        'https://m.media-amazon.com/images/I/610cp-BYVIL._SX522_.jpg',
    ],
    store_id=5,
    category_name="Health & beauty"
),
Product(
    title="Ultimate Detox Clay Mask",
    description="Purify your skin with the Ultimate Detox Clay Mask. This mask draws out impurities, reduces excess oil, and tightens pores, leaving your skin feeling refreshed and rejuvenated. Suitable for all skin types, it promotes a clearer, healthier complexion.",
    price=30.00,
    quantity=70,
    images=[
        'https://m.media-amazon.com/images/I/711y5U0HE1L._SX679_.jpg',
        'https://m.media-amazon.com/images/I/91oY5RQAHEL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/61cw3af3s4L._SX679_.jpg',
        'https://m.media-amazon.com/images/I/91YCz-zyoDL._SX679_.jpg',
    ],
    store_id=5,
    category_name="Health & beauty"
),
Product(
    title="Luxe Lashes Mascara",
    description="Enhance your lashes with Luxe Lashes Mascara. This long-lasting, smudge-proof mascara adds volume, length, and definition, giving you stunning, dramatic eyes. Its gentle formula ensures your lashes stay healthy and strong.",
    price=20.00,
    quantity=90,
    images=[
        'https://m.media-amazon.com/images/I/51M0aDgGYkL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/61VIvhv+RCL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/61otH3tE+5L._SX679_.jpg',
        'https://m.media-amazon.com/images/I/41RMiWwTvcL._SX679_.jpg'
    ],
    store_id=5,
    category_name="Health & beauty"
),
Product(
    title="HydraBoost Moisturizer",
    description="Keep your skin hydrated with HydraBoost Moisturizer. This lightweight, non-greasy formula provides all-day moisture, leaving your skin feeling soft, smooth, and nourished. Perfect for daily use, it enhances your skin's natural radiance.",
    price=35.00,
    quantity=120,
    images=[
        'https://m.media-amazon.com/images/I/71wUhQVqYmL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/617HVsCuAZL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/61t4-sn6TGL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/61155DoWAoL._SX679_.jpg'
    ],
    store_id=5,
    category_name="Health & beauty"
),
Product(
    title="RevitalEyes Eye Cream",
    description="Brighten and rejuvenate your eyes with RevitalEyes Eye Cream. This powerful cream reduces the appearance of dark circles, puffiness, and fine lines, leaving your eye area looking refreshed and youthful.",
    price=40.00,
    quantity=60,
    images=[
        'https://m.media-amazon.com/images/I/51jvFibcYAL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/51C+JulU-ML._SX679_.jpg',
        'https://m.media-amazon.com/images/I/51LezVoWqbL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/51VbL7O3CHL._SX679_.jpg'
    ],
    store_id=5,
    category_name="Health & beauty"
),
Product(
    title="Zen Aroma Diffuser",
    description="Create a relaxing atmosphere with the Zen Aroma Diffuser. This sleek, ultrasonic diffuser disperses essential oils into the air, filling your space with soothing scents. Perfect for enhancing your wellness routine and promoting relaxation.",
    price=50.00,
    quantity=75,
    images=[
        'https://m.media-amazon.com/images/I/313MV+RxcvL._SY300_SX300_.jpg',
        'https://m.media-amazon.com/images/I/51L3hR74WjL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/61gcrtwfZNL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/81HdkIEkDdL._SX679_.jpg'
    ],
    store_id=5,
    category_name="Health & beauty"
),
Product(
    title="GlowUp Vitamin C Serum",
    description="Brighten your skin with GlowUp Vitamin C Serum. This potent serum reduces the appearance of dark spots, evens out skin tone, and boosts collagen production, giving you a radiant, youthful complexion.",
    price=50.00,
    quantity=100,
    images=[
        'https://m.media-amazon.com/images/I/41vt4dLDz+L._SX679_.jpg',
        'https://m.media-amazon.com/images/I/51NOAWnnyHL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/41G7SFD5wRL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/31eK7YrqRQL._SX300_SY300_QL70_FMwebp_.jpg'
    ],
    store_id=5,
    category_name="Health & beauty"
),










Product(
    title="SoundMaster Wireless Headphones",
    description="Experience crystal clear sound with SoundMaster Wireless Headphones. Featuring noise-canceling technology, long battery life, and a comfortable fit, these headphones are perfect for music lovers and professionals alike.",
    price=120.00,
    quantity=200,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/files/JBL520BT-i5_600x.jpg?v=1697625150',
        'https://www.digitalstore.co.ke/cdn/shop/files/JBL520BT-i4_1000x.jpg?v=1697625151',
        'https://www.digitalstore.co.ke/cdn/shop/files/JBL520BT-i3_600x.jpg?v=1697625150',
        'https://www.digitalstore.co.ke/cdn/shop/files/JBL520BT-i1_1000x.jpg?v=1697625151'
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="HyperCharge Portable Charger",
    description="Keep your devices powered on the go with the HyperCharge Portable Charger. With a high-capacity battery and fast charging capabilities, this charger ensures your phone, tablet, and other gadgets stay charged throughout the day.",
    price=40.00,
    quantity=300,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/products/Supercharger1_1000x.jpg?v=1623071946',
        'https://www.digitalstore.co.ke/cdn/shop/products/Supercharger2_1600x.jpg?v=1623059315',
        'https://www.digitalstore.co.ke/cdn/shop/products/Supercharger3_1600x.jpg?v=1623059315',
        'https://www.digitalstore.co.ke/cdn/shop/products/Supercharger4_1600x.jpg?v=1623059315'
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="ProCam 4K Action Camera",
    description="Capture every adventure in stunning detail with the ProCam 4K Action Camera. This compact, durable camera is waterproof and comes with a range of accessories to help you shoot from any angle.",
    price=150.00,
    quantity=150,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/files/GoProHERO12BlackActionCamera-i1_1000x.webp?v=1703660853',
        'https://www.digitalstore.co.ke/cdn/shop/files/GoProHERO12BlackActionCamera-i2_1600x.webp?v=1703660852',
        'https://www.digitalstore.co.ke/cdn/shop/files/GoProHERO12BlackActionCamera-i4_1600x.webp?v=1703660853',
        'https://www.digitalstore.co.ke/cdn/shop/files/GoProHERO12BlackActionCamera-i5_1600x.webp?v=1703660853'
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="SmartHome WiFi Plug",
    description="Turn your home into a smart home with the SmartHome WiFi Plug. Control your appliances remotely, set schedules, and save energy with this easy-to-use smart plug compatible with Alexa and Google Assistant.",
    price=25.00,
    quantity=400,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/products/5576-320-1_1000x.jpg?v=1584172803',
        'https://www.digitalstore.co.ke/cdn/shop/products/5576-320-2_1000x.jpg?v=1584172804',
        'https://www.digitalstore.co.ke/cdn/shop/products/5576-320-3_1000x.jpg?v=1584172804',
        'https://www.digitalstore.co.ke/cdn/shop/products/5576-320-4_1000x.jpg?v=1584172804'
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="NextGen Smartwatch",
    description="Stay connected and track your fitness with the NextGen Smartwatch. Featuring a sleek design, heart rate monitoring, GPS, and compatibility with both iOS and Android, this smartwatch is perfect for your active lifestyle.",
    price=200.00,
    quantity=250,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/products/AmazfitGTR3Smartwatch-i1_800x.png?v=1663577286',
        'https://www.digitalstore.co.ke/cdn/shop/products/AmazfitGTR3Smartwatch-i2_800x.png?v=1663577287',
        'https://www.digitalstore.co.ke/cdn/shop/products/AmazfitGTR3Smartwatch-i3_800x.png?v=1663577286',
        'https://www.digitalstore.co.ke/cdn/shop/products/AmazfitGTR3Smartwatch-i4_800x.png?v=1663577286'
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="EcoSound Bluetooth Speaker",
    description="Enjoy your music anywhere with the EcoSound Bluetooth Speaker. This portable speaker delivers powerful sound, has a long-lasting battery, and is water-resistant, making it perfect for outdoor adventures.",
    price=60.00,
    quantity=500,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/files/SoundLink-i1_500x.jpg?v=1712831443',
        'https://www.digitalstore.co.ke/cdn/shop/files/SoundLink-i2_500x.jpg?v=1712831443',
        'https://www.digitalstore.co.ke/cdn/shop/files/SoundLink-i3_500x.jpg?v=1712831443',
        'https://www.digitalstore.co.ke/cdn/shop/files/SoundLink-i4_500x.jpg?v=1712831443'
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="UltraHD Streaming Device",
    description="Upgrade your entertainment system with the UltraHD Streaming Device. Stream your favorite shows and movies in stunning 4K quality, with support for all major streaming services and voice control functionality.",
    price=70.00,
    quantity=300,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/products/CHROMECAST-1_1000x.jpg?v=1559123404',
        'https://www.digitalstore.co.ke/cdn/shop/products/CHROMECAST-2_1600x.jpg?v=1559123405',
        'https://www.digitalstore.co.ke/cdn/shop/products/CHROMECAST-3_1600x.jpg?v=1559123408',
        'https://www.digitalstore.co.ke/cdn/shop/products/CHROMECAST-4_1600x.jpg?v=1559123409'
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="VisionGuard Blue Light Glasses",
    description="Protect your eyes from harmful blue light with VisionGuard Blue Light Glasses. These stylish glasses reduce eye strain and improve sleep quality by blocking blue light from screens.",
    price=30.00,
    quantity=350,
    images=[
        'https://m.media-amazon.com/images/I/6176ov3p4nL._SX679_.jpg',
        'https://m.media-amazon.com/images/I/617z623eRvL._SX569_.jpg'
        'https://m.media-amazon.com/images/I/614ZRiqajlL._SX569_.jpg',
        'https://m.media-amazon.com/images/I/617z623eRvL._SX569_.jpg',
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="MaxPower Laptop Charger",
    description="Never run out of power with the MaxPower Laptop Charger. This universal charger is compatible with most laptops and provides fast, reliable charging, making it an essential accessory for students and professionals.",
    price=45.00,
    quantity=150,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/products/1_ba5781ce-f4fd-4729-bcaf-88c406bb6341_1000x.jpg?v=1660722500',
        'https://www.digitalstore.co.ke/cdn/shop/products/1d_67f7b699-ae08-4602-a634-0ee5465876f0_1000x.jpg?v=1660722499',
        'https://www.digitalstore.co.ke/cdn/shop/products/oo_1000x.jpg?v=1660715127',
        'https://www.digitalstore.co.ke/cdn/shop/products/oo1_1000x.jpg?v=1660715126'
    ],
    store_id=6,
    category_name="Electronics"
),

Product(
    title="GamerPro Mechanical Keyboard",
    description="Enhance your gaming experience with the GamerPro Mechanical Keyboard. Featuring customizable RGB lighting, durable keys, and anti-ghosting technology, this keyboard is perfect for serious gamers.",
    price=80.00,
    quantity=100,
    images=[
        'https://www.digitalstore.co.ke/cdn/shop/files/GProMechanicalKeyboard-i5_1000x.jpg?v=1698072302',
        'https://www.digitalstore.co.ke/cdn/shop/files/GProMechanicalKeyboard-i1_1000x.jpg?v=1698072302',
        'https://www.digitalstore.co.ke/cdn/shop/files/GProMechanicalKeyboard-i2_500x.jpg?v=1698072302',
        'https://www.digitalstore.co.ke/cdn/shop/files/GProMechanicalKeyboard-i3_1000x.jpg?v=1698072302'
    ],
    store_id=6,
    category_name="Electronics"
)

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