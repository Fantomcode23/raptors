from wtforms.validators import Length
from restaurant import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        return user
    manager = RestaurantManager.query.get(int(user_id))
    return manager

# USER TABLE


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    fullname = db.Column(db.String(length=30), nullable=False)
    address = db.Column(db.String(length=50), nullable=False)
    phone_number = db.Column(db.Integer(), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    tables = db.relationship('Table', backref='reserved_user', lazy=True)
    items = db.relationship('Item', backref='ordered_user', lazy=True)
    orders = db.relationship('Order', backref='order_id_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

# TABLE RESERVATION TABLE


class Table(db.Model):
    __tablename__ = 'tables'

    table_id = db.Column(db.Integer(), primary_key=True)
    table = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.String(length=20), nullable=False)
    date = db.Column(db.String(length=20), nullable=False)
    accomodation = db.Column(db.Integer(), nullable=False)
    reservee = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def assign_ownership(self, user):
        self.reservee = user.id
        db.session.commit()

# MENU TABLE


class Item(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=50), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    source = db.Column(db.String(length=30), nullable=False)
    orderer = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def assign_ownership(self, user):
        self.orderer = user.id
        db.session.commit()

    def remove_ownership(self, user):
        if self.orderer == user.id:
            self.orderer = None
            db.session.commit()

# ORDERS TABLE


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    address = db.Column(db.String(length=50), nullable=False)
    order_items = db.Column(db.String(length=300), nullable=False)
    datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)

    def set_info(self, user, item):
        self.name = user.fullname
        self.address = user.address
        self.order_items = item.name
        self.user_id = user.id
        db.session.commit()

# CART TABLE
class Cart(db.Model):
    __tablename__ = 'carts'
    cart_id = db.Column(db.Integer(), primary_key=True)
    item_name = db.Column(db.String(length=30), nullable=False)
    item_price = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

    def set_info(self, user, item_name, item_price):
        self.user_id = user.id
        self.item_name = item_name
        self.item_price = item_price
        db.session.commit()

# Restaurant Manager Table

class RestaurantManager(db.Model, UserMixin):
    __tablename__ = 'restaurant_managers'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    fullname = db.Column(db.String(length=30), nullable=False)
    restaurant_name = db.Column(db.String(length=30), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
