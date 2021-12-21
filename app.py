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
    sessionId = db.Column(db.String(6), primary_key = True)
    testLevel = db.Column(db.Integer)
    realLevel = db.Column(db.Integer)
    certificate = db.Column(db.Boolean)
    liked = db.Column(db.Boolean)
    feedback = db.Column(db.Text)

    def __init__(self, sessionId, testLevel, realLevel, certificate, liked, feedback):
        self.sessionId = sessionId
        self.testLevel = testLevel
        self.realLevel = realLevel
        self.certificate = certificate
        self.liked = liked
        self.feedback = feedback

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

numberOfQuestions = 1

@app.route("/start", methods=['POST'])
def index():
    initTest = test.Test()
    sessionId = id_generator()
    type = "ask"
    word = initTest.getWord()
    step = initTest.currentCall
    returnDict = {"type": type,
                  "sessionId": sessionId,
                  "word": word,
                  "step": step}
    return jsonify(returnDict)

@app.route("/answer", methods=['POST'])
def continueTest():
    data = request.json
    sessionId = data["sessionId"]
    continueTest = test.Test()
    continueTest.setAnswers(data["history"])
    word = continueTest.getWord()
    step = continueTest.currentCall
    type = "continue"
    if step <= numberOfQuestions:
        returnDict = {"type": type,
                      "sessionId": sessionId,
                      "step": step,
                      "word": word,
                      "history": data["history"]}
    else:
        returnDict = {"type": "result",
                      "sessionId": sessionId,
                      "level": int(continueTest.levels[continueTest.currentCall])}
    return jsonify(returnDict)
    
@app.route("/form", methods=['POST'])
def stopTest():
    data = request.json
    sessionId = data ["sessionId"]
    testLevel = data["testLevel"]
    realLevel = data["realLevel"]
    certificate = data["certificate"]
    liked = data["liked"]
    feedback = data["feedback"]

    userFeedback = Feedback(sessionId, testLevel, realLevel, certificate, liked, feedback)
    db.session.add(userFeedback)
    db.session.commit()
    resp = jsonify(success=True)
    return resp

if __name__ == '__main__':
    app.run(debug=True)
