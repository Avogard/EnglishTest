from flask import Flask, render_template, request, flash
from flask_restful import Api, Resource
from flask import jsonify
import test

app = Flask(__name__)
api = Api(app)
app.secret_key = "manbearpig_MUDMAN888"


@app.route("/hello")
def index():
   flash("what's your name?")
   return render_template("index.html")

t = test.Test()

@app.route("/test", methods=['POST', 'GET'])
def greeter():
##    flash("Hi " + str(request.form['name_input']) + ", great to see you!")
    word = t.getWord()
    yes = request.form.get('Yes')
    if yes is not None:
        t.getAnswer(1)
    else:
        t.getAnswer(0)
    sendMessage = ""
    if t.currentCall == 10:
        sendMessage = "Your level is " + toCefr(t.levels[t.currentCall])
        t.clear()
    else:
        sendMessage = word
    return render_template("index.html", message = sendMessage)

def toCefr(level):
    cefr = ""
    if level == 1:
        cefr = "A1"
    if level == 2:
        cefr = "A2"
    if level == 3:
        cefr = "B1"
    if level == 4:
        cefr = "B2"
    if level == 5:
        cefr = "C1"
    if level == 6:
        cefr = "C2"
    return cefr
# names = {"me":          {"Lol": True},
#         "someoneElse":  {"Lol": False}}

# class HelloWorld(Resource):
#     def get(self):
#         return ({'ip': request.remote_addr}), 200

# api.add_resource(HelloWorld, "/")


# if __name__ == "__main__":
#     app.run(debug=True)