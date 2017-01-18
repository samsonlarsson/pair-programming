from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required
from .forms import SessionForm
from . import main
from app import db
from ..models import User, CodeSession
from app.email import send_email
from firebase import firebase
from slackclient import SlackClient


session_url = ""
@main.route('/')
def index():
    session.permanent = True
    return render_template('main/home.html')

def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None


def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

# Send message
def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username=current_user.username,
        icon_emoji=':robot_face:'
    )

# Recieving messages
@main.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
    return Response(), 200


@main.route('/', methods=['GET'])
def test():
    return Response('It works!')


#Initiates a new session on user request
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

#Sends out the request via an email for code pairing
#Queries for all the users currently registered for pairing
@main.route('/session', methods=['GET', 'POST'])
@login_required
def session():
    users = User.query.all()
    if request.method == 'POST':
        for user in users:
            if str(user.username+' ') == str(request.form.get('usernames')):
                print user.username
                session_link = request.form.get('session_link')
                send_email(current_user.email, user.email, "Pear Invite", 'mail/invite', user=user,  current_user=current_user,
                           session_link=session_link)
                print str(session_link)
    return render_template('main/session.html', users=users)

#Queries the firebase for all the existing session
#Checks for sessions created by current_user and renders the session in table
@main.route('/sessions')
@login_required
def my_session():
        fire = firebase.FirebaseApplication('https://pear-1dd83.firebaseio.com/')
        results = fire.get('https://pear-1dd83.firebaseio.com/', None)
        sess_hash = []
        for result in results:
            for x in results[result]:
               if str(current_user.username) == str(results[result][x].get('username')).strip():
                   sess_hash.append(str(results[result][x].get('session')))
        return render_template('main/my_sessions.html', sess_hash=sess_hash)

#Gets the session from firebase and loads its instance
#Uses the hashed key to track each session
@main.route('/edit/<hashed>')
def edit(hashed):
    global session_url
    #TODO followup
    session_url = "http://pearpro.herokuapp.com/session#"+hashed
    return redirect(session_url)

#Queries the firebase database for the session Id and deletes it from firebase
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


if __name__ == '__main__':
    channels = list_channels()
    if channels:
        print("Channels: ")
        for channel in channels:
            print(channel['name'] + " (" + channel['id'] + ")")
            detailed_info = channel_info(channel['id'])
            if detailed_info:
                print('Latest text from ' + channel['name'] + ":")
                print(detailed_info['latest']['text'])
            if channel['name'] == 'general':
                send_message(channel['id'], "Hello " +
                             channel['name'] + "! It worked!")
        print('-----')
    else:
        print("Unable to authenticate.")