from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json

from website import db
from website.models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required  # you can not go to the home page unless you logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  # we loaded the request as json, not form
    note = json.loads(request.data)  # take data from post request, loaded as json or python dictionary
    noteId = note['noteId']  # access to noteId attribute
    note = Note.query.get(noteId)  # get the primary id
    if note:
        if note.user_id == current_user.id:  # if this user that signed in , has this note
            db.session.delete(note)
            db.session.commit()
    return jsonify({})  # turn it to an json object, here e return an empty object because we need to return something
