from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import Required, Length
from ..models import User
from slackclient import SlackClient

class SessionForm(Form):
    session_name = StringField(
        'Session name', validators=[Required(), Length(1, 64)])
    language = SelectField(u'Programming Language', choices=[('py', 'Python')])
    submit = SubmitField('Create session')

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class ChatForm(Form):
    channel = SelectField(u'Channel', choices=[()])
    text = StringField('Enter Message here', validators=[Required()])
    submit = SubmitField('Send')
        

#TODO Implement in future @samson
class EditProfileAdminForm(Form):

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
