import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 's8d7678fhg0jn96fdhf7547dfgdsg7dsf8h69fd75jsf7g86gfd9g8f7s6h978j59s6f8sd76fh7s8d')
