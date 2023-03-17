from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route('/', methods=['POST', 'GET'])
def start_survey():
    title = satisfaction_survey.title
    instruction = satisfaction_survey.instructions
    return render_template('start.html', title=title, instruction=instruction)

@app.route('/questions/0', methods=["POST", "GET"])
def first_question():
    question = satisfaction_survey.questions[0]
    question_text = question.question
    if request.method == "POST":
        session['RESPONSES'] = []
        answer = request.form['answer']
        results = session['RESPONSES']
        results.append(answer)
        print(results)
        return redirect(url_for('questions', index=1))
    return render_template('first_question.html', question=question_text )

@app.route('/questions/<int:index>', methods=["GET", "POST"])
def questions(index):
    question = satisfaction_survey.questions[index]
    question_text = question.question
    if request.method == "POST":
        answer = request.form['answer']
        results = session['RESPONSES']
        results.append(answer)
        print(results)
        if index == len(satisfaction_survey.questions) - 1:
            return redirect(url_for('thanks'))
        else:
            return redirect(url_for('questions', index=index + 1))
    return render_template('first_question.html', question=question_text )

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


