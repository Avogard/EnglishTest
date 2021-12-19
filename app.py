from flask import Flask, request, flash
from flask.globals import session
from flask import jsonify
import test
import string
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mvzckqkdrsceou:73feffa9d938b7c7e80d15d49bb1634bf3fc729494186203708d3259c54f541a@ec2-3-95-130-249.compute-1.amazonaws.com:5432/d3d5elk79fhfat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key = True)
    test = db.Column(db.String(200))

    def __init__(self, test):
        self.test = test

app.secret_key = "manbearpig_MUDMAN888"

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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

wrapper = test.testWrapper()
numberOfQuestions = 25

@app.route("/start", methods=['POST'])
def index():
    sessionId = id_generator()
    wrapper.createTest(sessionId)
    type = "ask"
    word = wrapper.tests[sessionId].getWord()
    step = wrapper.tests[sessionId].currentCall
    data = {"word": word,
            "step": step}
    returnDict = {"type": type,
                  "sessionId": sessionId,
                  "data": data}
    return jsonify(returnDict)

@app.route("/answer", methods=['POST'])
def continueTest():
    data = request.json
    sessionId = data.get("sessionId", "MISSING INPUT ID")
    # currentTest = wrapper.tests.get(sessionId, "MISSING TEST KEY")
    # if currentTest == "MISSING TEST KEY":
        # return jsonify({"message": "missing test key", "Data": data, "WrapperTest": wrapper.tests})
    # currentTest.setAnswer(data["answer"])
    # word = currentTest.getWord()
    # step = currentTest.currentCall
    # data = {"word": word,
            # "step": step}
    # if step <= numberOfQuestions:
    returnDict = {"type": "ask",
                  "sessionId": sessionId,
                #   "data": data,
                  "numberQuestions": numberOfQuestions,
                  "wrapper": type(wrapper).__name__}
    # else:
    #     returnDict = {"type": "result",
    #                   "sessionId": sessionId,
    #                   "data": {"level": toCefr(currentTest.levels[currentTest.currentCall])}}
    return jsonify(returnDict)
    
@app.route("/form", methods=['POST'])
def stopTest():
    data = request.json
    sessionId = data["sessionId"]
    resp = jsonify(success=True)
    del wrapper.tests[sessionId]
    return resp

if __name__ == '__main__':
    app.run()
