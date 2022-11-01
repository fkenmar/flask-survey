from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = "cowsarecool69"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)


responses = []


@app.route("/")
def start_direct():
    # return redirect("/question/0")
    title = satisfaction_survey.title
    instruction = satisfaction_survey.instructions
    return render_template("start.html", title=title, instruction=instruction)


@app.route('/question')
def start_button():
    qnum = len(responses) + 1
    if qnum < 5:
        return redirect(f"/question/{qnum}")
    else:
        return redirect("/thankyou")


@app.route('/question/<int:qnum>')
def question(qnum):
    if qnum == 5:
        return redirect("/thankyou")
    if qnum != len(responses) + 1:
        flash("Invalid URL!")
        return redirect(f"/question/{len(responses)+1}")
    qnum = len(responses)
    questions = satisfaction_survey.questions[qnum].question
    text = satisfaction_survey.questions[qnum].allow_text
    choices = satisfaction_survey.questions[qnum].choices
    return render_template("questions.html", qnum=qnum, questions=questions, text=text, choices=choices)


@app.route('/answer', methods=["POST"])
def answer():
    selected = request.form['choice_selected']
    responses.append(selected)
    return redirect('/question')


@app.route("/thankyou")
def thank():
    return render_template("thanks.html")
