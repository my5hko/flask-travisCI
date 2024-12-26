from flask_swagger import swagger
from collections import OrderedDict

def build_swagger(app):
    swg = swagger(app)
    swg["info"]["title"] = "Expense control app"
    swg["info"]["version"] = "0.0.1"
    swg["definitions"] = {
        "Hello": {
            "type": "object",
            "discriminator": "HelloType",
            "properties": {
                "message": {"type": "string"}
            },
            "example": {
                "message": "Hello, I'm the app to calulate expenses!"
            },
        },
        "Home":{
            "type": "object",
            "discriminator": "HomeType",
            "properties": {
                "message": {"type": "string"},
            },
            "example": {
                "Message": "Expense calculation app",
            }
        },
        "ExpenseIn" : {
            "type": "object",
            "discriminator": "ExpenseInType",
            "properties": OrderedDict({
                "title": {"type": "string"},
                "amount": {"type": "number"}
            }),
            "example": OrderedDict({
                "title": "Your expense",
                "amount": 0,
            })
        },
        "ExpenseOut": {
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"}
                    },
                    "example" : {
                        "id" : 0
                    }
                }
            ]
        },
        "UserIn" : {
            "type": "object",
            "discriminator": "UserInType",
            "properties": OrderedDict({
                "username": {"type": "string"},
                "password": {"type": "string"}
            }),
            "example": {
                "username": "mr_user",
                "password": "mr_password"
            },
        },
        "UserOut": {
            "type": "object",
            "discriminator": "UserOutType",
            "properties": {
                "id": {"type": "number"},
                "username": {"type": "string"}
            },
            "example" : {
                "id" : 1,
                "username": "mr_user"
            },
        },
        "TokenOut": {
            "type": "object",
            "discriminator": "TokenOutType",
            "properties": {
                "access_token": {"type": "string"}
            },
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzE5Mjg4MzIsImlhdCI6MTYzMTkyODQzMiwibmJmIjoxNjMxOTI4NDMyLCJpZGVudGl0eSI6MX0.4a5c5e0"
            },
        },
        "Unauthorized": {
            "type": "object",
            "discriminator": "UnauthorizedType",
            "properties": {
                "error": {"type": "string"}
            },
            "example": {
                "error": "You are not authorized for this action"
            },
        },
        "NotFound":{
            "type": "object",
            "discriminator": "NotFoundType",
            "properties": {
                "error": {"type": "string"},
                        },
            "example": {
                "error": "Could not find this expense/user :(",
            }
        }
    }
    return swg