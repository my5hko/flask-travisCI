from flask import Blueprint, request, jsonify #importing Blueprint class, request object, jsonify function from flask

from app.schemas import user_schema     #importing user_schema from app.schemas
from app.db import db, User #importing db and User from app.db
from marshmallow import ValidationError #importing ValidationError from marshmallow
from werkzeug.security import generate_password_hash #importing generate_password_hash from werkzeug.security
from werkzeug.security import check_password_hash #importing check_password_hash from werkzeug.security
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
 
 
bp = Blueprint("user", __name__, url_prefix="/users") #creating Blueprint for users where name is user, 
#import name is __name__ and url_prefix is /users, so all URIs will start with /users

@bp.route("/", methods=["POST"]) #URI to create new user, method POST in Blueprint
def register():  #function to create new user
    """
    New user creation
    ---
    tags:
        - user
    produces:
        - application/json
    parameters:
        - name: user
          in: body
          description: User data
          required: true
          schema:
            $ref: '#/definitions/UserIn'
    responses:
        201:
            description: User created
            schema:
                $ref: '#/definitions/UserOut'
        400:
            description: Missing required fields
        422:
            description: Validation error
        409:
            description: Username already exists
    """
    json_data = request.json #creating data directly from incoming json
    if not json_data: # Check if json_data is None
        return {"message": "No input data provided"}, 400 #returning message and status code

    try:
        data = user_schema.load(json_data) #loading data from json
    except ValidationError as err: #if data is not valid
        return jsonify(err.messages), 422   #returning error message and status code

    if not isinstance(data, dict): # Check if data is a dictionary
        return {"message": "Invalid data format"}, 400

    username = data.get("username") # Get username from data
    password = data.get("password") # Get password from data

    if username is None or password is None: # Check if username or password is None
        return {"message": "Missing required fields"}, 400 #returning message and status code

    try:
        new_user = User( #creating new instance of User class with username and password taken from data dict
            username=username, # Username is taken from data earlier 
            password=generate_password_hash(password, method="pbkdf2") # Get password from data and generate hash using generate_password_hash with password and method pbkdf2
        )
        db.session.add(new_user) # Add new instance to db
        db.session.commit() # Commit session
    except IntegrityError as err: #if username already exists when IntegrityError is raised
        db.session.rollback() # Rollback session
        return jsonify(error="Username already exists"), 400 #returning message and status code

    return jsonify(message="User created successfully", user=user_schema.dump(new_user)), 201 #, 
#    return jsonify(user_schema.dump(new_user)), 201


@bp.route("/login", methods=["POST"])
def login(): #function to login user
    """
    User login
    ---
    tags:
        - user
    produces:
        - application/json
    parameters:
        - name: user
          in: body
          description: User login
          required: true
          schema:
            $ref: '#/definitions/UserIn'
    responses:
        200:
            description: User logged in successfully
            schema:
                $ref: '#/definitions/TokenOut'
        401:
            description: Invalid username or password
            schema:
                $ref: '#/definitions/Unauthorized'
        404:
            description: User not found
            schema:
                $ref: '#/definitions/NotFound'
        422:
            description: Validation error

    """

    json_data = request.json #creating data directly from incoming json
    if not json_data: #check if json_data exists
        return {"message": "No input data provided"}, 400
    
    try:
        data = user_schema.load(json_data) #loading data from json
    except ValidationError as err: #if data is not valid
        return jsonify(err.messages), 422  #returning error message and status code
    
#Suggested by Copilot
    if not isinstance(data, dict): # Check if data is a dictionary
        return {"error": "Invalid data format"}, 400

    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return {"errror": "Missing required fields"}, 400

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        return {"error": "Invalid username or password"}, 401

#From training
    # user = db.first_or_404(db.select(User).filter_by(username=data["username"]) ) # Get user from db by username using first_or_404 method with select and filter_by methods

    # if not check_password_hash(user.password, data["password"]): # Check if password is correct
    #     return jsonify(error="Invalid username or password"), 401 #returning message and status code
    
    access_token = create_access_token(identity=user.username) # Create access token with user.username
    return jsonify(access_token=access_token)


