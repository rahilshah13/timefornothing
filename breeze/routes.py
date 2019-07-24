import os, secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from breeze import app, db, bcrypt, mail
from breeze.forms import RegistrationForm, LoginForm, PostForm, EmailForm
from breeze.models import User, Post, Email
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_mail import Message


@app.route("/", methods=['GET', 'POST'],)
@app.route("/home", methods=['GET', 'POST'],)
def index():
    file = open("ip.txt","a+")
    file.write(request.environ.get('HTTP_X_REAL_IP', request.remote_addr)+" - "+str(datetime.utcnow())+"\n")
    file.close()
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route("/about", methods=['GET', 'POST'],)
def about():
    return render_template('about.html')

@app.route("/contact", methods=['GET', 'POST'],)
def contact():
    return render_template('index.html')

def send_email():
    emails = Email.query.all()
    email_list = []

    for e in emails:
        email_list.append(e.email)

    msg = Message('time for nothing!', sender=('time for nothing', 'timefornothingwc@gmail.com'), recipients=email_list) 
    msg.body = "a new chapter is out! go check it out at https://tinyurl.com/timefornothing"
    mail.send(msg)

@app.route("/emaillist", methods=['GET', 'POST'],)
def updates():
    form = EmailForm()
    if form.validate_on_submit():
        email = Email(email= form.email.data)
        db.session.add(email)
        db.session.commit()
        flash(f'Email Updates Added for {form.email.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('email.html', form=form)


@app.route("/signup", methods=['GET', 'POST'],)
@login_required
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email= form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route("/admin", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/chapters', picture_fn)
    form_picture.save(picture_path)
    # output_size = (125, 125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)
    return picture_fn


@app.route("/newpost", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.comic.data)
        post = Post(title=form.title.data, content=form.content.data, author=current_user, image_file=picture_file)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        send_email()
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def read_post(post_id):
    post = Post.query.get_or_404(post_id)
    image_file = url_for('static', filename='chapters/' + post.image_file)
    return render_template('post.html', post=post, image_file=image_file)


@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
