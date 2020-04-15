from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Table for user info such as contact info password and username
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#Table to link Users and the cards they are watching
#UserCard = db.Table('UserCard',
 #   userId = db.Column(db.Integer, db.ForeignKey('user.id')),
  #  cardId = db.Column(db.Integer, db.ForeignKey('card.id'))
#)

#Card info such as version and name
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardName = db.Column(db.String(32), index=True)
    cardSet = db.Column(db.String(32), index=True)
    results =  db.relationship('Results', backref='cardname', lazy='dynamic')
    
    def __repr__(self):
        return '<Card {}>'.format(self.cardName)

#Webscrape results, will get info every 2 hours
class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    cardId  = db.Column(db.Integer, db.ForeignKey('card.id'))
    siteId = db.Column(db.Integer, db.ForeignKey('site.id'))
    searchTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #card = db.relationship('Card', backref='price', lazy='dynamic')

    def __repr__(self):
        return '<Search {}>'.format(self.price)

#Sites for webscraps, used to show where prices come from
class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siteLink = db.Column(db.String(32), unique=True, index=True)
    siteName = db.Column(db.String(32), unique=True, index=True)
    results = db.relationship('Results', backref='results', lazy='dynamic')

    def __repr__(self):
        return self.siteLink


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
