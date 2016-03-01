from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("contents.html")

@app.route("/valueCPM")
def valueCPM():
	return render_template("valueCPM/valueCPM.html")

@app.route("/profile/<username>")
def profile(username):
	return "Hey there %s" % username

if __name__ == "__main__":
	app.run(debug=True)