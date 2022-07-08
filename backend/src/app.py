import os
from turtle import title
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
''' 
#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
def getDrink():
    drinks = Drink.query.order_by(Drink.id).all()

    try:
        formattedDrink = [drink.short() for drink in drinks ]
        return {"success": True, "drinks": formattedDrink}

    except Exception as e:
        print(e)
        abort(422)    

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def getDrinkDetail(payload):
    
    drinks = Drink.query.order_by(Drink.id).all()
    try:

        formattedDrink = [drink.long() for drink in drinks ]
        return {"success": True, "drinks": formattedDrink}

    except Exception as e:
        print(e)
        abort(422)    

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def createNewDrink(payload):
        drinks = ''
        # Get data from the received request
        body = request.get_json()

        list = []

        # Get each data from the body object
        newTitle = body.get("title", None)
        newRecipe = body.get("recipe", None)

        #using json dump to convert object properties to double quotes
        recipeDump = json.dumps(newRecipe)
        #add to the empty array
        list.append(recipeDump)
        #convert the list to a string
        stringRecipe = ' '.join(str(x) for x in list)
        #concatenate braces to facilitate json fetching
        formattedRecipe = "[" + stringRecipe + "]"


        try:
            drink = Drink(
                title = newTitle,
                recipe = formattedRecipe
            )
            drink.insert()


        except Exception as e:
            print(e)
            abort(422)
        
        drinks = Drink.query.filter(Drink.title == newTitle).all()
        formattedDrink = [drink.long() for drink in drinks ]

        return {"success": True, "drinks": formattedDrink}

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def updateDrink(payload, id):
    
        # Get data from the database
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        # Get data from the received request
        body = request.get_json()

        # Get each data from the body object
        title = body.get("title", None)

        if drink is None:
            abort(404)

        try:
            drink.title = title
            drink.update()


        except Exception as e:
            print(e)
            abort(402)
        
        drinks = Drink.query.filter(Drink.title == title).all()
        formattedDrink = [drink.long() for drink in drinks ]

        return {"success": True, "drinks": formattedDrink}

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleteDrink(payload, id):

        # Get data from the database
        drink = Drink.query.filter(Drink.id == id).one_or_none()


        if drink is None:
            abort(404)

        try:
            drink.delete()


        except Exception as e:
            print(e)
            abort(422)
        
        return {"success": True, "delete": id}

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )

@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )

@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    )


@app.errorhandler(401)
def invaild_credentials(error):
    return (
        jsonify({"success": False, "error": 401, "message": "credentials invalid"}), 401
    )


@app.errorhandler(403)
def no_permission(error):
    return (
        jsonify({"success": False, "error": 403, "message": "permission not found"}), 403
    )

@app.errorhandler(405)
def not_found(error):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed"}),
        405,
    )


@app.errorhandler(500)
def server_error(error):
    return (
        jsonify({"success": False, "error": 500, "message": "Internal server error"}),
        500,
    )







'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
