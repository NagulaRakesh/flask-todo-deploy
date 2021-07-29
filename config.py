import os

class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
    'postgresql://localhost/mac'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
