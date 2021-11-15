from flask import Flask, render_template, request, flash
import test

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

##@app.route("/hello")
##def index():
##    flash("what's your name?")
##    return render_template("index.html")

@app.route("/greet", methods=['POST', 'GET'])
def greeter():
##    flash("Hi " + str(request.form['name_input']) + ", great to see you!")
    t = test.Test()
    flash("Do you know this word? " + t.getWord())
    t.getAnswer(1)
    return render_template("index.html")
