#!/usr/bin/python3
import json
from flask import Flask, request, make_response, jsonify
from models import Users, User, Game, LoginException

app = Flask(__name__)

# Arseny: using global conditions like `users` and variables like `game`
# Arseny: is a bad software design pattern. Using global variables like
# Arseny: `game` is really bad. It's not solution is not scalable.
# Arseny: What to use instead of this? For example try create new class 
# Arseny: Which inherit `Flask`. Add to this properties for `users` and
# Arseny: `game`
users = Users()
game = None

@app.route('/')
def index():
    return 'Hello world'

@app.route('/login', methods=['POST'])
def login():

    try:
        users.add_user(request.json['login'])
    except LoginException as err: 
        return make_response(jsonify(status=err.message), 400)

    # Arseny: better practice for logging is using module `logging`
    # Arseny: from python standart library
    print(users)

    return jsonify(status="ok")

@app.route('/create-game', methods=['POST'])
def create_game():

    global game

    if not users.user_exist(request.json['login']):
        return make_response(jsonify(status='wrong login'), 400)
    
    if game is None:
        game = Game()
        user = users.get_user(request.json['login'])
        game.join_user(user)

        print(game)

        return jsonify(status='ok')
    else:
        return make_response(jsonify(status='game is already on'), 400)


@app.route('/join-game',methods=['POST'])
def join_game():

    global game

    if not users.user_exist(request.json['login']):
        return make_response(jsonify(status='wrong login'), 400)

    if game is None:
        return make_response(jsonify(status="game doesn't exist"), 400)

    if game.user_joined(request.json['login']):
        return make_response(jsonify(status='user already joined'), 400)

    user = users.get_user(request.json['login'])
    game.join_user(user)
    print(game)

    return jsonify(status='ok')


app.run()