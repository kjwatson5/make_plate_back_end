from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Food, food_schema, foods_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/food', methods = ['POST'])
@token_required
def create_food(current_user_token):
    main_course = request.json['main_course']
    vegetable = request.json['vegetable']
    side_dish = request.json['side_dish']
    dessert = request.json['dessert']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    food = food(main_course, vegetable, side_dish, dessert, user_token = user_token)

    db.session.add(food)
    db.session.commit()

    response = food_schema.dump(food)
    return jsonify(response)

@api.route('/food', methods = ['GET'])
@token_required
def get_food(current_user_token):
    a_user = current_user_token.token
    foods = Food.query.filter_by(user_token = a_user).all()
    response = foods_schema.dump(foods)
    return jsonify(response)


@api.route('/food/<id>', methods = ['GET'])
@token_required
def get_single_food(current_user_token, id):
    food = Food.query.get(id)
    response = food_schema.dump(food)
    return jsonify(response)

# Update endpoint
@api.route('/food/<id>', methods = ['POST', 'PUT'])
@token_required
def update_food(current_user_token, id):
    food = Food.query.get(id)
    food.main_course = request.json['main_course']
    food.vegetable = request.json['vegetable']
    food.side_dish = request.json['side_dish']
    food.dessert = request.json['dessert']
    food.user_token = current_user_token.token

    db.session.commit()
    response = food_schema.dump(food)
    return jsonify(response)

# Delete endpoint
@api.route('/food/<id>', methods = ['DELETE'])
@token_required
def delete_food(current_user_token, id):
    food = Food.query.get(id)
    db.session.delete(food)
    db.session.commit()
    response = food_schema.dump(food)
    return jsonify(response)
