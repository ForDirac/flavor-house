from datetime import datetime
from .core import server

db = server.db


class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), nullable=False)
  user_id = db.Column(db.String(100), nullable=False, index=True)
  password = db.Column(db.String(200), nullable=False, index=True)
  join_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  # relations
  user_store_relation = db.relationship('Favorites', backref='users', lazy='dynamic')


class Stores(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  category = db.Column(db.String(100), nullable=False)
  description = db.Column(db.String(1000))
  score = db.Column(db.Float)
  # relations
  store_user_relation = db.relationship('Favorites', backref='stores', lazy='dynamic')
  store_review_relation = db.relationship('Reviews', backref='stores', lazy='dynamic')
  store_tag_relation = db.relationship('StoreTags', backref='stores', lazy='dynamic')


class Favorites(db.Model):
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), primary_key=True)
  date = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Reviews(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
  content = db.Column(db.String(1000))
  likes = db.Column(db.Integer, nullable=False, default=0)
  date = db.Column(db.DateTime, nullable=False)
  #add
  score = db.Column(db.Float)


class Tags(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False, index=True)
  # relations
  tag_store_relation = db.relationship('StoreTags', backref='tags', lazy='dynamic')


class StoreTags(db.Model):
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)