from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.thoughts import Thought

@app.route('/createThought', methods=['POST'])
def createThought():

    if not Thought.validate_thoughts(request.form):
        return redirect(request.referrer)
    data = {
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Thought.create_thoughts(data)
    return redirect('/')

@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'thoughts_id': id,
        'user_id': session['user_id']
    }
    Thought.addLike(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'thoughts_id': id,
        'users_id': session['user_id']
    }
    Thought.removeLike(data)
    return redirect(request.referrer)

@app.route('/delete/<int:id>')
def destroyThought(id):
    data = {
        'thoughts_id': id,
    }
    thoughts = Thought.get_thoughts_by_id(data)
    if session['user_id']==thoughts['creator_id']:
        Thought.deleteAllLikes(data)
        Thought.destroythoughts(data)
        return redirect(request.referrer)
    return redirect(request.referrer)