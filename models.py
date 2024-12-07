import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv('DATABASE_URL')
db = SQLAlchemy()

def setup_db(app, database_url=database_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    with app.app_context():
        db.init_app(app)
        db.create_all()

class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    movie_id = Column(Integer, db.ForeignKey('movies.id'), nullable=True)
    movie = db.relationship('Movie', backref='actors', lazy=True)
    
    def __init__(self, name, age, gender, movie_id, movie):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id
        self.movie = movie
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id,
            'movie': self.movie.format()
        }