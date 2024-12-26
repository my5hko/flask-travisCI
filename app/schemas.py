from marshmallow import Schema, fields, validate

class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0.01)
    )

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)

class UserSchema(Schema): #creating schema class for user
    id = fields.Int(dump_only=True) #field for id, only for dumping (can only be returned, do not accepting input)
    username = fields.Str( #field for username, string type
        required=True, #required field
        validate=validate.Length(min=3, max=50) #validating length of the username
    )
    password = fields.Str( #field for password, string type
        required=True, #required field
        load_only = True, #only for loading (not returning)
        validate=validate.Length(min=4) #validating length of the password
    )

user_schema = UserSchema() #creating instance of UserSchema for single user