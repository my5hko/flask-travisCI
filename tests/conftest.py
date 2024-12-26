import os #importing os module to be able to get config type from environment variables
import pytest #importing pytest
from werkzeug.security import generate_password_hash #importing generate_password_hash function from werkzeug.security

from app.db import db, User, Expense #importing db, User and Expense from app.db

from app import create_app #importing create_app function from app

@pytest.fixture(scope = "module") #decorator to create fixture for module scope
def test_client(): #function to create test client
    os.environ["CONFIG_TYPE"] = "app.config.TestConfig" #setting CONFIG_TYPE environment variable to app.config.TestConfig
    flask_app = create_app() #creating flask app using create_app function

    with flask_app.test_client() as testing_client: #to get test client from flask app, can send requests to Flask app
        with flask_app.app_context(): #using context manager to get app context to
            yield testing_client 
#return test client using yield instead of return as we nned to return it as generator to be able to return multiple values

@pytest.fixture(scope = "module") #decorator to create fixture for module scope
def new_user():
   return User(username="test_user", password="test_password") #returning new user with username test_user and password test_password 

@pytest.fixture(scope = "module") #decorator to create fixture for module scope
def init_database(test_client): #function to initialize database
    db.create_all()   #creating all tables in db
    
    defaul_user = User(username="def_user", password = generate_password_hash("test_password", method="pbkdf2")) #creating default 
    #user with username def_user and password test_password in hashed form witn pbkdf2 method, because Travis CI does not support scrypt method from Python 3.12

    second_user = User(username="second_user", password = generate_password_hash("test_password", method="pbkdf2"))

    db.session.add(defaul_user) #adding default user to db
    db.session.add(second_user) #adding second user to db
    db.session.commit() #commiting session

    expense1 = Expense(title="Expense1", amount=10, user_id = defaul_user.id) #creating new instance of Expense class with title test_expense1 and amount 100 and user_id from default user
    expense2 = Expense(title="Expense2", amount=20, user_id = defaul_user.id)
    expense3 = Expense(title="Expense3", amount=30, user_id = defaul_user.id)
    db.session.add_all([expense1, expense2, expense3]) #adding all instances to db
    db.session.commit() 

    yield #code above should be executed before the test, code below - after the test

    db.drop_all() #cleaning up after the test

@pytest.fixture(scope = "module") #decorator to create fixture for module scope
def default_user_token(test_client):
    response = test_client.post("/users/login", json={"username": "def_user", "password": "test_password"})

    yield response.json["access_token"] #returning access token for default user

@pytest.fixture(scope = "module") #decorator to create fixture for module scope
def second_user_token(test_client):
    response = test_client.post("/users/login", json={"username": "second_user", "password": "test_password"})

    yield response.json["access_token"] #returning access token for default user