from flask import Flask, redirect, render_template, session, flash, url_for, request
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:walmart48@localhost/auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'somesecretkey'

connect_db(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def show_users():
    """Redirect to /register"""

    return redirect('/register')

@app.route('/register', methods=['GET'])
def show_register():
    """Show register form"""
    form = RegisterForm()    
    if 'username' in session:
        return redirect(url_for('userinfo', username=session.get('username')))
    else:
        return render_template('register_form.html', form=form)

@app.route('/register', methods=['POST'])
def register():
    """Register user"""
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        return redirect(url_for('userinfo', username=session.get('username')))
    
    return redirect('/register')
    
@app.route('/login', methods=['GET'])
def show_login():
    """Show login form"""
    form = LoginForm()

    if 'username' in session:
        return redirect(url_for('userinfo', username=session.get('username')))
    else:
        return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def login():
    """Login user"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(url_for('userinfo', username=session.get('username')))
        else:
            return redirect('/login')
        
    return redirect('/login')
    
@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('username')

    return redirect('/login')    

@app.route('/users/<username>')
def userinfo(username):
    """Show user info and feedback"""

    user = User.query.filter_by(username=username).first()

    if 'username' not in session:
        return redirect('/login')
    elif session['username'] != username:
        # redirect to the user's own page
        return redirect(url_for('userinfo', username=session.get('username')))
    else:
        return render_template('user_info.html', user=user, feedback=user.feedback)
    
@app.route('/users/<username>/feedback/add', methods=['GET'])
def show_feedback_form(username):
    """Show feedback form"""
    form = FeedbackForm()

    if 'username' not in session:
        return redirect('/login')
    elif session['username'] != username:
        # redirect to the user's own page
        return redirect(url_for('userinfo', username=session.get('username')))
    else:
        return render_template('feedback_form.html', form=form)
    
@app.route('/users/<username>/feedback/add', methods=['POST'])
def add_feedback(username):
    """Add feedback"""
    form = FeedbackForm()

    if form.validate_on_submit() and session['username'] == username:
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(url_for('userinfo', username=username))
    
    return redirect(url_for('show_feedback_form', username=username))

@app.route('/feedback/<int:feedback_id>/update')
def show_update_feedback_form(feedback_id):
    """Show update feedback form"""
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if session['username'] == feedback.username:
        return render_template('feedback_form.html', form=form)
    
    return redirect(url_for('userinfo', username=session.get('username')))

@app.route('/feedback/<int:feedback_id>/update', methods=['POST'])
def update_feedback(feedback_id):
    """Update feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit() and session['username'] == feedback.username:
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(url_for('userinfo', username=feedback.username))
    
    return redirect(url_for('userinfo', username=session.get('username')))

@app.route('/feedback/<int:feedback_id>/delete', methods=['GET', 'POST'])
def delete_feedback(feedback_id):
    """Delete feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username

    if session['username'] == username:
        db.session.delete(feedback)
        db.session.commit()

        return redirect(url_for('userinfo', username=username))
    
    return redirect(url_for('userinfo', username=session.get('username')))

@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def delete_user(username):
    """Delete user"""
    user = User.query.filter_by(username=username).first()

    if session['username'] == username:
        # delete feedback that belongs to the user
        feedback = Feedback.query.filter_by(username=username).all()
        for f in feedback:
            db.session.delete(f)

        # delete user
        db.session.delete(user)
        db.session.commit()

        return redirect('/logout')
    
    return redirect(url_for('userinfo', username=session.get('username')))