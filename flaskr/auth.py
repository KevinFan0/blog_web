import functools
import pdb
from flask import (Blueprint,flash,g,
                   redirect,render_template,request,session,url_for)

from werkzeug.security import check_password_hash,generate_password_hash
from flaskr.db import get_db
from werkzeug.exceptions import abort

#定义蓝图
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        school = request.form['school']
        role_id = request.form['role']
        
        if role_id == "superuser":
            role_id = 1
        else:
            role_id = 2
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not gender:
            error = 'Gender is required.'
        elif not school:
            error = 'School is required.'
        elif db.execute('SELECT id FROM user WHERE username = ?',(username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password, gender, school, role_id) VALUES (?,?,?,?,?)', (username, generate_password_hash(password), gender, school, role_id))
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/users',methods=('GET','POST'))
@login_required
def get_users():
    # if request.method == 'POST':
    db = get_db()
    posts = db.execute('SELECT id,username,gender,school,role_id FROM user').fetchall()
    return render_template('auth/users.html', posts=posts)


def get_user(id,check_auth=True):
    user = get_db().execute('SELECT id,username,gender,school,role_id FROM user WHERE id = ?', (id,)).fetchone()

    if user is None:
        abort(404,"Post id {0} doesn't exist.".format(id))
    return user


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_user(id)
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('auth.get_users'))