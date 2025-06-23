from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
# type: ignore
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

# Entry model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_entry = db.Column(db.Date, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    group_name = db.Column(db.String(150), nullable=False)
    details = db.Column(db.Text, nullable=False)
    tape_number = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/admin', methods=['GET'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    entries = Entry.query.order_by(Entry.date_of_entry.desc()).all()
    return render_template('admin_dashboard.html', entries=entries)

@app.route('/user', methods=['GET'])
@login_required
def user_dashboard():
    entries = Entry.query.order_by(Entry.date_of_entry.desc()).all()
    return render_template('user_dashboard.html', entries=entries)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/add', methods=['POST'])
@login_required
def admin_add_entry():
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    date_of_entry = request.form['date_of_entry']
    username = request.form['username']
    group_name = request.form['group_name']
    details = request.form['details']
    tape_number = request.form['tape_number']
    entry = Entry(  # type: ignore
        date_of_entry=datetime.strptime(date_of_entry, '%Y-%m-%d'),
        username=username,
        group_name=group_name,
        details=details,
        tape_number=tape_number
    )
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_entry(id):
    if current_user.role != 'admin':
        return redirect(url_for('user_dashboard'))
    entry = Entry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# Utility to create admin user (run once)
@app.cli.command('create-admin')
def create_admin():
    username = input('Enter admin username: ')
    password = input('Enter admin password: ')
    if User.query.filter_by(username=username).first():
        print('Admin already exists!')
        return
    admin = User(username=username, password=generate_password_hash(password), role='admin')
    db.session.add(admin)
    db.session.commit()
    print('Admin user created!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 