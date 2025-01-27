from flask import Flask, render_template, request, redirect, url_for, flash
from app.face_recognition import register_user, verify_user
from app.voting import process_vote
from app.blockchain_utils import register_on_blockchain, record_vote

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        if register_user(name):
            register_on_blockchain(name)
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Registration failed. Try again.', 'danger')
    return render_template('register.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        voter = verify_user()
        if voter:
            representative = request.form['representative']
            record_vote(voter, representative)
            flash(f'Thank you for voting, {voter}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Voter verification failed.', 'danger')
    return render_template('vote.html')

if __name__ == '__main__':
    app.run(debug=True)
