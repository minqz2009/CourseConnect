from flask_login import UserMixin
from dan import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    reviews = db.relationship('CourseReview', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CourseReview(db.Model):
    __tablename__ = "coursereview"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(128))
    review = db.Column(db.String(128))
    rating = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=True)
    user_grade = db.Column(db.Integer)

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=False)
    code = db.Column(db.String(16), nullable=False, unique=True)
    rating = db.Column(db.Integer)
    reviews = db.relationship('CourseReview', backref='course', lazy=True)

