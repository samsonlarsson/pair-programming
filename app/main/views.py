from flask import render_template, redirect, url_for, request
from flask.ext.login import current_user, login_required
from .forms import SessionForm
from . import main
from app import db
from ..models import User, CodeSession
from app.email import send_email
from firebase import firebase


session_url = ""
@main.route('/')
def index():
    session.permanent = True
    return render_template('main/home.html')


@main.route('/new', methods=['GET', 'POST'])
def new_session():
    form = SessionForm()
    if form.validate_on_submit():
        session_ = CodeSession(session_name=form.session_name.data, session_lang=form.language.data)
        if current_user.id is not None:
            user_ = User.query.get(current_user.id)
            user_.sessions.append(session_)
            db.session.add(user_)
            db.session.commit()
        return redirect(url_for('main.session'))
    return render_template('main/new_session.html', form=form)


@main.route('/session', methods=['GET', 'POST'])
@login_required
def session():
    users = User.query.all()
    if request.method == 'POST':
        for user in users:
            if str(user.username+' ') == str(request.form.get('usernames')):
                print user.username
                session_link = request.form.get('session_link')
                msg = " Hello {} you have an invite from {} to a pair programming. Please follow this link to access the session\n {}".format(use.username, current_user.usernam, session_link)
                send_email(sender = current_user.email, msg = msg, receipent = user.email)
                print str(session_link)
    return render_template('main/session.html', users=users)


@main.route('/sessions')
@login_required
def my_session():
        fire = firebase.FirebaseApplication('https://pear-1dd83.firebaseio.com/')
        results = fire.get('https://pear-1dd83.firebaseio.com/', None)
        sess_hash = []
        
        try:
            for result in results:
                for x in results[result]:
                    if str(current_user.username) == str(results[result][x].get('username')).strip():
                        sess_hash.append(str(results[result][x].get('session')))
            return render_template('main/my_sessions.html', sess_hash=sess_hash)
        except:
            print results   


@main.route('/edit/<hashed>')
def edit(hashed):
    global session_url
    #TODO followup
    session_url = "https://pear-1dd83.firebaseio.com/session#"+hashed
    return redirect(session_url)


@main.route('/delete/<hashed>')
@login_required
def delete(hashed):
    fire = firebase.FirebaseApplication('https://pear-1dd83.firebaseio.com/')
    results = fire.get(current_user.username + '  ', None)
    for result in results:
        print results[result]
        if results[result].get('session') == hashed:
            fire.delete(current_user.username + '  ', result)
    return redirect(url_for('main.my_session'))


@main.route('/chat')
@login_required
def chat():
    return redirect('http://127.0.0.1:5001')

