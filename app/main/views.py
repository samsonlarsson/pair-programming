from flask import render_template, redirect, url_for, request
from flask.ext.login import current_user, login_required
from .forms import SessionForm
from . import main
from app import db
from ..models import User, CodeSession
from app.email import send_email
from firebase import firebase


