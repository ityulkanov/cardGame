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
app.users = Users()
app.game = None

@app.route('/')
def index():
    return 'Hello world'

@app.route('/login', methods=['POST'])
def login():
    try:
        user = User(request.json['login'])
        app.users.add_user(user)
    except LoginException as err: 
        return make_response(jsonify(status=err.message), 400)

    print(app.users)

    return jsonify(status="ok")

@app.route('/create-game', methods=['POST'])
def create_game():
    if not app.users.user_exist(request.json['login']):
        return make_response(jsonify(status='wrong login'), 400)
    
    if app.game is None:
        app.game = Game()
        user = app.users.get_user(request.json['login'])
        app.game.join_user(user)

        print(app.game)

        return jsonify(status='ok')
    else:
        return make_response(jsonify(status='game is already on'), 400)


@app.route('/join-game', methods=['POST'])
def join_game():
    if not app.users.user_exist(request.json['login']):
        return make_response(jsonify(status='wrong login'), 400)

    if app.game is None:
        return make_response(jsonify(status="game doesn't exist"), 400)

    if app.game.user_joined(request.json['login']):
        return make_response(jsonify(status='user already joined'), 400)

    user = app.users.get_user(request.json['login'])
    app.game.join_user(user)
    print(app.game)

    return jsonify(status='ok')


@app.route('/ready', methods=['POST'])
def ready():
    if not app.users.user_exist(request.json['login']):
        return make_response(jsonify(status='wrong login'), 400)

    if app.game is None:
        return make_response(jsonify(status="game doesn't exist"), 400)

    if not app.game.user_joined(request.json['login']):
        return make_response(jsonify(status="user isn't joined"), 400)

    user = app.game.users.get_user(request.json['login'])
    user.ready = True

    if app.game.all_users_ready() and app.game.users.users_count >= 2:
        app.game.start_turn()

    return make_response(jsonify(status='ok'), 200)


@app.route('/rising', methods=['POST'])
def rising():
    #TODO: verification
    user = app.game.users.get_user(request.json['login'])
    rising_value = request.json['data']

    if not user.money - rising_value >= 0:
        return make_response(jsonify(status='not enough money'))

    if rising_value - app.game.actual_bet < app.game.blind:
        return make_response(jsonify(status='rise is small then blind'))

    user.bet = rising_value
    app.game.actual_bet = rising_value
    app.game.next_player()

    return make_response(jsonify(status='ok'), 200)


@app.route('/call', methods=['POST'])
def call():
    #TODO: verification
    user = app.game.users.get_user(request.json['login'])

    if not user.money - user.bet >= app.game.actual_bet:
        return make_response(jsonify(status='not enough money'), 400)

    user.bet = app.game.actual_bet
    app.game.next_player()

    return make_response(jsonify(status='ok'), 200)


@app.route('/check', methods=['POST'])
def check():
    #TODO: create check functional
    return make_response(jsonify(status='ok'), 200)


@app.route('/fold', methods=['POST'])
def fold():
    #TODO: create fold functional
    return make_response(jsonify(status='ok'), 200)


@app.route('/state', methods=['POST'])
def state():
    if not app.users.user_exist(request.json['login']):
        return make_response(jsonify(status='wrong login'), 400)

    active_user = app.users.get_user(request.json['login']).__dict__.copy()

    users = [user.__dict__.copy() for user in app.game.users]
    users = list(filter(lambda x: x['login'] != active_user['login'], users))

    if app.game.game_status == 'ON':
        for user in users:
            user['cards'] = ['X','X']

    game = app.game.__dict__.copy()
    game['user'] = active_user
    game['users'] = users

    print(game)
    return make_response(jsonify(status=game), 200)


app.run()