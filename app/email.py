from flask import current_app, render_template, redirect
from flask.ext.mail import Message
from threading import Thread
from .import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)



def send_email(sender, to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['PEAR_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=sender, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr