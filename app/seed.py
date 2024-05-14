from flask_bcrypt import Bcrypt
from app import app
from models import db, User, Store
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
           
        print("Seeding users...")
        users = [
            User(username="Peter Mwongela", email="peter@gmail.com", password=bcrypt.generate_password_hash("Peter.123").decode('utf-8'), role='seller', image='https://images.pexels.com/photos/819530/pexels-photo-819530.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0712345678"),
            User(username="Hamdi Adan", email="hamdi@gmail.com", password=bcrypt.generate_password_hash("Hamdi.123").decode('utf-8'),  role='seller', image='https://images.pexels.com/photos/764529/pexels-photo-764529.jpeg?auto=compress&cs=tinysrgb&w=600',contact="0723456789"),
            User(username="Alex Mambo", email="alex@gmail.com", password=bcrypt.generate_password_hash("Alex.123").decode('utf-8'),  role='buyer', image='https://images.pexels.com/photos/11506216/pexels-photo-11506216.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0734567890"),
            User(username="Louis Oduor", email="louis@gmail.com", password=bcrypt.generate_password_hash("Louis.123").decode('utf-8'), role='buyer', image='https://images.pexels.com/photos/20434986/pexels-photo-20434986/free-photo-of-jasmine-bajwa-model-shoot.jpeg?auto=compress&cs=tinysrgb&w=600',contact="0787654321"),
            User(username="Candy Bosibori", email="candy@gmail.com", password=bcrypt.generate_password_hash("Candybosibori.123").decode('utf-8'), role='buyer', image='https://images.pexels.com/photos/8864285/pexels-photo-8864285.jpeg?auto=compress&cs=tinysrgb&w=600', contact="0798765432")
        ]

        db.session.add_all(users)
        db.session.commit()    
        print("Done seeding!")