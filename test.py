# Arseny: when you write tests the good practice is
# Arseny: using the `pytest` lib or the `unittest` lib
from server import index, login, create_game, join_game
import models

def assertIndex(): 
	assert index() == "Hello world"

# Arseny: did you run this? There is a syntax error! Function without "()"
def assertLogin(): 
	#this function to work requires user import, how do I test it the? same with the rest 	
	assert login() == ""

# Arseny: there is syntax error too
def assertcreate_game():
	assert create_game() == ""

# Arseny: and there
def join_game(): 
	assert join_game() == ""

#Here is a testing block for models file

#testing Users class: 

def assertUsers_userExist():
	assert Users.user_exist() == ""

def assertUsers_addUser():
	assert Users.add_user() == ""

def assertUsers_getUser():
	assert Users.get_user() == ""

#testing Game class: 

def assertGame_userJoined():
	assert Game.user_joined() == ""

def assertGame_joinUser():
	assert Game.join_user() == ""