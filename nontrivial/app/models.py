from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

following_assoc = db.Table('following-assoc',
    db.Column('user_id', db.Integer, db.ForeignKey('user-table.id')),
    db.Column('item_ud', db.Integer, db.ForeignKey('item-table.id'))
    )

class User(UserMixin, db.Model):
    __tablename__ = 'user-table'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    listings = db.relationship("Listing", back_populates="owner")
    following = db.relationship("Item", secondary=following_assoc, back_populates="followers")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Listing(db.Model):
    __tablename__ = 'listing-table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(256), nullable=False)
    price = db.Column(db.String(32), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('user-table.id'))
    owner = db.relationship("User", back_populates="listings")
    item_id = db.Column(db.Integer, db.ForeignKey('item-table.id'))
    item = db.relationship("Item" , back_populates="item_listings")

class Item(db.Model):
    __tablename__ = 'item-table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(256), nullable=False)

    item_listings = db.relationship("Listing", back_populates="item")
    followers = db.relationship("User", secondary=following_assoc, back_populates="following")