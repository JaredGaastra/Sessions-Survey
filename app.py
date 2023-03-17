from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route('/', methods=["POST", "GET"])
def choose_survey():
    if request.method == 'POST':
        if 'survey-types' in request.form:
            survey_type = request.form['survey-types']
            if survey_type == 'satisfaction':
                # Start satisfaction survey
                survey = satisfaction_survey
                return redirect(url_for('start_survey', survey_type=survey_type))
            elif survey_type == 'personality':
                # Start personality quiz
                survey = personality_quiz
                return redirect(url_for('start_survey', survey_type=survey_type))
    return render_template('choose.html')


@app.route('/<survey_type>', methods=['POST', 'GET'])
def start_survey(survey_type):
    if survey_type == 'satisfaction_survey':
        survey = satisfaction_survey
    else:
        survey = personality_quiz
    

    title = survey.title
    instruction = survey.instructions
    return render_template('start.html', title=title, instruction=instruction)

@app.route('/questions/<int:index>', methods=["GET", "POST"])
def first_question(index):
    survey_type = session.get('survey_type')
    if survey_type == 'satisfaction_survey':
        survey = satisfaction_survey
    else:
        survey = personality_quiz
    
    question = survey.questions[index]
    question_text = question.question

    if request.method == "POST":
        answer = request.form['answer']
        responses = session['responses']
        responses.append(answer)
        session['responses'] = responses

        if index == len(survey.questions) - 1:
            return redirect(url_for('thanks'))
        else:
            return redirect(url_for('first_question', index=index + 1))

    return render_template('first_question.html', question=question_text)

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


