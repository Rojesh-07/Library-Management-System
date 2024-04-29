import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from LMS import app, db, bcrypt
from LMS.forms import RegistrationForm, LoginForm, UpdateAccountForm, addbookForm, Search
from LMS.models import User,Book, BorrowBook
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    Boo = Book.query.all()
    return render_template('home.html',booklist=Boo)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register as User', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture2(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # borrow_data = BorrowBook.query.all()
    borrow_data = BorrowBook.query.filter_by(user_name=current_user.username).all()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, borrow_data=borrow_data)

@app.route("/AdminDashboard")
@login_required
def AdminDashboard():
    num_books = Book.query.count()
    return render_template('admindash.html', total_books=num_books)

@app.route("/addbook", methods=['GET', 'POST'])
@login_required
def addbook():
    form = addbookForm()
    if form.validate_on_submit():
        picture_file = save_picture2(form.image_file.data)
        book = Book(name=form.book_name.data, content=form.content.data, author=form.author_name.data, image_file=picture_file)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to the page where books are displayed
    return render_template('addbook.html', title='Register as User', form=form)


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = Search()
    if form.validate_on_submit():
        book = Book.query.filter_by(name=form.book_name.data).first()
        if book:
            return redirect(url_for('show_book', book_id=book.id))
        else:
            flash('Book not found!', 'danger')
            return redirect(url_for('search'))
    return render_template('search.html', form=form)

@app.route("/book/<int:book_id>")
@login_required
def show_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.name,
                           image_file=book.image_file,
                           content=book.content,
                           author=book.author
                           )


@app.route('/borrow', methods=['POST'])
def borrow_book():
    bookname = request.form['bookname']
    username = current_user.username

    book = Book.query.filter_by(name=bookname).first()
    if book:
        # Assuming BorrowBook is a model for tracking borrowed books
        borrow = BorrowBook(book_name=bookname, user_name=username)
        db.session.add(borrow)
        db.session.commit()
        flash('Book borrowed successfully!', 'success')
    else:
        flash('Book not available for borrowing!', 'danger')

    return redirect(url_for('home'))


@app.route("/browse_books")
@login_required
def browse_books():
    data = Book.query.all()
    print(data)
    return render_template('browse_book.html', borrow_book=data)

from openai import OpenAI
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

@app.route('/chat', methods=['POST','GET'])
def chat():
    print("Chat")
    return render_template('Chatbot.html')

@app.route('/Chatbot', methods=['POST','GET'])
def Chatbot():
    user_input = request.json['user_input']
    print(user_input)
    print("Received user input:", user_input)  # Debugging message

@app.route('/process', methods=['POST'])
def process():
    user_input = request.json['user_input']
    print("Received user input:", user_input)  # Debugging message

    # Call OpenAI API
    completion = client.chat.completions.create(
        model="google/gemma-7b",
        messages=[{"role":"user","content":str(user_input)}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )

    output = ''
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            output += chunk.choices[0].delta.content

    return jsonify({'output': output})