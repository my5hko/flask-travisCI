from flask_jwt_extended import JWTManager #importing JWTManager from flask_jwt_extended\
from app.db import User #importing User from app.db

jwt = JWTManager()  #creating instance of JWTManager

# creating these functions to be able to access data about identity of user and to be able to get user identity from anywhere in the app
@jwt.user_identity_loader #decorator to get user identity
def user_identity_lookup(username): #function to get user identity
    return username #returning username

@jwt.user_lookup_loader #decorator to get user from db by username
def uswr_lookup_callback(jwt_header, jwt_data): #function to get user identity
    identity = jwt_data["sub"] # Get user identity from jwt_data from sub key
    return User.query.filter_by(username=identity).one_or_none() #returning user from db by username with filter_by method 
#and one_or_none method, that will return None if no user is found or one user if found
