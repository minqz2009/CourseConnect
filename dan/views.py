from dan import app, db
from dan.models import User, CourseReview, Course
from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from dan.forms import LoginForm, RegistrationForm, ReviewForm, CourseSearchForm
import datetime

@app.route('/course/<int:course_id>')
def course(course_id):
    course = Course.query.get(course_id)


    return render_template('course.html', course=course)

@app.route('/course/<int:course_id>/review', methods=['GET', 'POST'])
@login_required
def course_review(course_id):
    form = ReviewForm()
    course = Course.query.get(course_id)
    if form.validate_on_submit():
        old_review = CourseReview.query.filter_by(course_id=course_id, user_id=current_user.id).delete()
        review = CourseReview(course_id=course_id, user_id=current_user.id
        , review=form.review.data, rating=form.rating.data, title=form.title.data
        , user_grade=form.user_grade.data, date=datetime.datetime.now())
        db.session.add(review)
        db.session.commit()

        rating_list = [review.rating for review in course.reviews]
        course.rating = sum(rating_list) / float(len(rating_list))
        flash('Review added', 'success')
        db.session.commit()

        return redirect(url_for('course', course_id=course.id))
    
    return render_template('course_review.html', course=course, form=form)

@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile_user(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@login_required
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    courses = Course.query.all()
    form = CourseSearchForm()
    if form.validate_on_submit():
        old_courses = courses
        courses = []
        for course in old_courses:
            if(form.course.data == '0'):
                if form.search.data.lower() in course.name.lower():
                    courses.append(course)
            else:
                if form.search.data.lower() in course.name.lower() and form.course.data.lower() in course.code.lower():
                    courses.append(course)

    return render_template('home.html', courses=courses, form=form)

# BOTH PATIENT AND DOCTOR
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user is not None and user.check_password(form.password.data)):
            login_user(user)
            flash('You have been logged in', 'success')
            return redirect(url_for("home"))
        else:
            flash('Login Unsuccessful. Please Try Again', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('User has been successfully registered', 'success')
        return redirect(url_for("register"))
    return render_template('register.html', form=form)
