from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user,login_user
from .models import Note
from .models import User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/page',methods=['GET','POST'])
def page():
    if request.method == 'POST':
        email = request.form.get('email')
        Name = request.form.get('Name')
        feedback = request.form.get('feedback')

        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('email must be greater then 3 characters.',category='error')
        elif len(Name) < 2:
            flash('Name must be greater then 1 character.',category='error')
        elif len(feedback)< 2:
            flash('feedback must be greatar then 1 character.',category='error')
        else:
            flash('Thank You for feedback',category='success')
            login_user(user, remember=True)
            return redirect(url_for('auth.login'))
    return render_template("page.html", user=current_user)
    


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
