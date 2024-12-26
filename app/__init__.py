from flask import Flask, jsonify
import json  #importing json module
import os #importing os module, to be able to get config type from environment variables

def create_app():
    app = Flask(__name__, instance_relative_config=True)
# section for configuration from config.py file
    config_type= os.getenv("CONFIG_TYPE", default="app.config.Config") 
    #getting config type from environment variables, if not found - using default value from config.py
    app.config.from_object(config_type) #setting config type to app.config.Config
   
# this section was used before creation of config.py file for base and test configurations   
    #app.config.from_mapping(SQLALCHEMY_DATABASE_URI="sqlite:///expenses.sqlite3", JWT_SECRET_KEY="jwt-super-secret") 
     #adding JWT_SECRET_KEY to app config to avoid error 500 during JWT token creation
    

    @app.route("/")
    def home():
        """ 
        Main page
        ---
        tags: 
            - homepage 
        produces:
            - application/json
        responses:
            200:
                description: Home
                schema: 
                    $ref: "#/definitions/Home"
        """
        
        return jsonify(message="Expense calculation app")
    
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify(error="Could not find this expense :("), 404
    
    from app.swagger_utils import build_swagger
    from app.swagger_bp import swagger_ui_blueprint, SWAGGER_API_URL

    @app.route(SWAGGER_API_URL)     #route for swagger API
    def spec():    #function that returns swagger API
        return json.dumps(build_swagger(app), sort_keys=False) 
    #returning swagger API as json with sort_keys=False to keep order of keys without sorting alphabetically 
#        return jsonify(build_swagger(app)) #returning swagger API as json
    
    from app.db import db #importing db from app.db
    from app.migrate import migrate #importing migrate from app.migrate
    from app.jwt import jwt #importing jwt from app.jwt


    db.init_app(app) #initializing db
    migrate.init_app(app, db, render_as_batch=True) #initializing migrate using init_app method with app, db and 
    #render_as_batch=True as arguments, where re render_as_batch=True - to render migrations as batch (needed for sqlite)
    jwt.init_app(app) #initializing jwt using init_app method with app as argument


    from app import expense #importing expense from app
    from app import user #importing user from app
    app.register_blueprint(expense.bp) #registering blueprint for expense
    app.register_blueprint(user.bp) #registering blueprint for user
    app.register_blueprint(swagger_ui_blueprint) #registering swagger blueprint

    return app #returning Flask app instance