from crypt import methods
from http.client import responses
from urllib import response
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

'''
Author: Mahad Osman
Date: Nov 17th
Updated: Nov 22 To include session.
Assignment: Flask Tools Exercise 
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False #Removing the consistent redirect
debug = DebugToolbarExtension(app)

#Setting up both our question and respons lists
questions = satisfaction_survey.questions
#session['RESPONSES'] = []



#This allows us to extract the questions in a list
#Using list comprehensions to extract the question questions and actual choices
questions_list = [question.question for question in questions]
choice_list = [question.choices for question in questions]

@app.route('/')
def show_home():
    ''' Our root path to show the start of the game'''
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("root.html", title = title, instructions = instructions)

@app.route('/start', methods=["POST"])
def start_survey():
    '''Start path which will pop in to reset our responses array than redirect to our first question
        - Updated to include our sessions.
        -Changed to post to push our session back up.
    '''
    session['RESPONSES'] = []
    # print("*********SESSION************")
    # print(session['RESPONSES'] )
    # print("*********SESSION************")
    return redirect("/questions/0")

@app.route('/questions/<int:id>')
def show_question(id):
    '''Handles all of our questions
        - Takes the id to indicate which question we are currently answering.
        - Will set our question and choice based on that.
        - Conditional logic to check if the game has been completed or if the user tries to skip to future questions.
    '''
    questions = questions_list[id]
    choices = choice_list[id]
    
    '''Setting our session variable to be used.'''
    responses =  session.get('RESPONSES') 

    #If they try and reach the end we will go thank
    if(len(responses) == len(questions_list)):
        return redirect("/thankyou")
    
    #If they try to change it to the incorrect question we will redivert them to the current id that need be answered
    if(len(responses) != id):
        #A quick flash message to let the user know not to change the url
        flash("Incorrect url, please fill out the survey in order.")
        return redirect (f"/questions/{len(responses)}")

    return render_template("question.html", questions = questions, choices = choices, id = id) 


@app.route('/answers', methods = ["POST"])
def import_answers():
    ''' Handles the answered data and appends it to our responses array.
        - It shall use the length of our responses to move forward to the next question that need be answered.
        - Once the survey is completed it shall redirect our user to our thank you page.
    '''
    answer = request.form["question"]

    '''Session addition. To add our session values we must first change it from a session variable to a list to append. Than add it bacl.'''
    responses = session['RESPONSES']
    responses.append(answer)
    session['RESPONSES'] = responses

    #print(responses)
    if(len(responses) == len(questions_list)):
        return redirect("/thankyou")
    else:
        return redirect (f"/questions/{len(responses)}")

@app.route('/thankyou')
def show_thanks():
    '''Simple function to display our thank you page upon survey completion.'''
    return render_template("thankyou.html")