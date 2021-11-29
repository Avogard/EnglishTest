from flask import Flask, request, flash
from flask.globals import session
from flask import jsonify
import test
import string
import random

app = Flask(__name__)
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
    currentTest = wrapper.tests.get(sessionId, "MISSING TEST KEY")
    if currentTest == "MISSING TEST KEY":
        return jsonify({"message": "missing test key"})
    currentTest.setAnswer(data["answer"])
    word = currentTest.getWord()
    step = currentTest.currentCall
    data = {"word": word,
            "step": step}
    if step <= numberOfQuestions:
        returnDict = {"type": "ask",
                      "sessionId": sessionId,
                      "data": data}
    else:
        returnDict = {"type": "result",
                      "sessionId": sessionId,
                      "data": {"level": toCefr(currentTest.levels[currentTest.currentCall])}}
    return jsonify(returnDict)
    
@app.route("/form", methods=['POST'])
def stopTest():
    data = request.json
    sessionId = data["sessionId"]
    resp = jsonify(success=True)
    del wrapper.tests[sessionId]
    return resp
