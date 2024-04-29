from datetime import datetime
from LMS import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Book(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Book('{self.name}')"
    
class BorrowBook(db.Model):
    book_name = db.Column(db.Integer, nullable=False, primary_key=True)
    user_name = db.Column(db.Integer, nullable=False, primary_key=True)
    date_borrowed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=7))

    def __repr__(self):
        return f"BorrowBook('{self.book.name}', '{self.user.username}', '{self.date_borrowed}', '{self.due_date}')"
