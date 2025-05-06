from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "flashcard_secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)

with open('flashcards.json') as f:
    flashcards = json.load(f)

@app.route('/')
def home():
    session.permanent = True
    session['score'] = 0
    session['index'] = 0
    random.shuffle(flashcards)
    return render_template('index.html', total=len(flashcards))

@app.route('/card')
def card():
    index = session.get('index', 0)
    if index >= len(flashcards):
        return jsonify({'done': True})
    card = flashcards[index]
    return jsonify({
        'question': card['question'],
        'answer': card['answer'],
        'index': index + 1,
        'total': len(flashcards)
    })

@app.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()
    correct = data.get('correct', False)
    if correct:
        session['score'] = session.get('score', 0) + 1
    session['index'] = session.get('index', 0) + 1
    return jsonify({'score': session['score']})

@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0), total=len(flashcards))

if __name__ == '__main__':
    app.run(debug=True)