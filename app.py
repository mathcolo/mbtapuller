from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/<string:route>")
def displayRoute(route):
	return "Current trains on the " + route + "line!" 
	
@app.route("/all")
def displayAll(route):
	return "All trains currently running!"

if __name__ == "__main__":
    app.run()

