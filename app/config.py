class Config: # Base Config class
    TESTING=False #testing flag
    SQLALCHEMY_DATABASE_URI="sqlite:///expenses.sqlite3"  #path to the app db
    JWT_SECRET_KEY="jwt-super-secret" #JWT secret key


class TestConfig(Config): #TestConfig class inherited from Config
    TESTING=True #testing flag
    SQLALCHEMY_DATABASE_URI="sqlite:///test.db" #path to test db