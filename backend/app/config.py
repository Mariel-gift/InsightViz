import os

class Config:
   
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mariel@localhost:5432/InsightViz'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
