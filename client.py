#I guess here shold be client side :) 
import requests
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/login", methods = ['POST'])
def login():
	userLogin = {'login':'vasya'}
	res = requests.post(url + 'login', json=userLogin)
	print(res.text)
	return jsonify(userLogin)

login()