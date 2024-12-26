from flask import Blueprint, request, jsonify
from app.db import Expense, db
from app.schemas import expense_schema, expenses_schema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user #jwt_required to check if user is authenticated, current_user to get current user

bp = Blueprint("expense", __name__, url_prefix="/expenses")


@bp.route("/", methods=["POST"]) #URI to create new expense, method POST in Blueprint
@jwt_required() #decorator to check if user is authenticated
def create_expense():
    """ 
    Create new expense
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
        - name : Authorization
          in: header
          description: JWT token
          required: true
        - name : expense
          in: body
          description: Expenses info
          required: true
          schema: 
            $ref: '#/definitions/ExpenseIn'
    responses:
        201:
            description: Created expense
            scheme:
                $ref: '#/definitions/ExpenseOut'
        401:
            description: No access
            schema:
                $ref: '#/definitions/Unauthorized'
        422:
            description: Validation error
       """
    json_data = request.json
    try:
        data = expense_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    new_expense = Expense(title=data["title"], amount=data["amount"], user_id=current_user.id)
    db.session.add(new_expense)
    db.session.commit()

    return jsonify(expense_schema.dump(new_expense)), 201

@bp.route("/", methods=["GET"])
@jwt_required() #decorator to check if user is authenticated
def get_expenses():
    """ 
    Returns expenses list
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
        - name : Authorization
          in: header
          description: JWT token
          required: true
    responses:
        200:
            description: Expenses list
            schema: 
                $ref: "#/definitions/ExpenseOut"
        401:
            description: No access
            schema:
                $ref: '#/definitions/Unauthorized'
       """
 #   expenses = Expense.query.all() #calling Expenses class and method query to get all data from db using metod all
#    return jsonify(expenses_schema.dump(expenses)), 200
    return jsonify(expenses_schema.dump(current_user.expenses)), 200

@bp.route("/<int:id>", methods=["GET"])
@jwt_required() #decorator to check if user is authenticated
def get_expense(id):
    """ 
    Returns expense details
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
        - name : Authorization
          in: header
          description: JWT token
          required: true
        - name : id
          in: path
          description: Expense details
          required: true
          type: number

    responses:
        200:
            description: Expense details
            schema: 
                $ref: "#/definitions/ExpenseOut"
        401:
            description: No access
            schema:
                $ref: '#/definitions/Unauthorized'
        404:
            description: Expense not found
            schema: 
                $ref: "#/definitions/NotFound"
    """
    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id: # Check if user is owner of the expense
        return jsonify(error="You are not allowed to view this expense"), 401 #returning message and status code

    return jsonify(expense_schema.dump(expense))

@bp.route("/<int:id>", methods=["PATCH"])
@jwt_required() #decorator to check if user is authenticated
def update_expense(id):
    """ 
    Update expense details
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
        - name : Authorization
          in: header
          description: JWT token
          required: true
        - name : id
          in: path
          description: Expense id
          required: true
          type: number
        - name : expense
          in: body
          description: New expense details
          required: true
          schema: 
            $ref: '#/definitions/ExpenseIn'
    responses:
        200:
            description: Expense updated
            schema: 
                $ref: "#/definitions/ExpenseOut"
        401:
            description: No access
            schema:
                $ref: '#/definitions/Unauthorized'
        404:
            description: Expense not found
            schema: 
                $ref: "#/definitions/NotFound"
        422:
            description: Validation error
    
    """
    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id: # Check if user is owner of the expense
        return jsonify(error="You are not allowed to view this expense"), 401 #returning message and status code
    json_data = request.json
    try:
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as err:
        return err.messages, 422
    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)

    db.session.commit()

    return jsonify(expense_schema.dump(expense))


@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required() #decorator to check if user is authenticated
def delete_expense(id):
    """ 
    Delete expense
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
        - name : Authorization
          in: header
          description: JWT token
          required: true
        - name : id
          in: path
          description: Expense id
          required: true
          type: number
    responses:
        204:
            description: Expense deleted
        401:
            description: No access
            schema:
                $ref: '#/definitions/Unauthorized'
        404:
            description: Expense not found
            schema: 
                $ref: "#/definitions/NotFound"        
    """
    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id: # Check if user is owner of the expense
        return jsonify(error="You are not allowed to view this expense"), 401 #returning message and status code
    db.session.delete(expense)
    db.session.commit()
    return "", 204