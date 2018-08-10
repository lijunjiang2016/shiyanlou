from flask import Flask, render_template, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
	username = request.cookies.get('username')
	return "hello, {}".format(username)

@app.route('/user/<username>')
def user_index(username):
	resp = make_response(render_template("user_index.html", username=username))
	resp.set_cookie('username', username)
	return resp

if __name__ == "__main__":
	app.run()

