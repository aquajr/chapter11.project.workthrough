from app import app, db
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, EditProfileForm, PostForm
from datetime import datetime


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form
    )




@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'] )
@login_required
def index():
    """Index url"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is live!')
        return redirect(url_for('index'))
    posts = Post.query.all()
    return render_template(
        'index.html',
        title='Home',
        form=form,
        posts=posts
    )




@app.route('/<username>/profile')
@login_required
def profile(username):
    """PROFILE PAGE"""
    user = User.query.filter_by(username=username).first_or_404()
    posts = current_user.posts.all()
    return render_template(
        'profile.html',
        title='Profile',
        user=user,
        posts=posts
    )



@app.route('/login', methods=['GET', 'POST'])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect (url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {form.username.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register URL"""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered successfuly. Login to continue')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)