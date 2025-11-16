from flask import Blueprint, render_template, request, redirect, url_for, flash # type: ignore
from flask_login import login_user, logout_user, login_required, current_user # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

# ======================
# Login
# ======================
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('notes.dashboard'))
            else:
                return redirect(url_for('notes.home'))
        else:
            flash("Username hoặc password không đúng!", "danger")
    return render_template('login.html')


# ======================
# Logout
# ======================
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ======================
# Register
# ======================
@bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Kiểm tra username/email tồn tại
        if User.query.filter_by(username=username).first():
            error = 'Username đã tồn tại!'
        elif User.query.filter_by(email=email).first():
            error = 'Email đã tồn tại!'
        else:
            user = User(username=username, email=email, is_admin=False)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Tạo tài khoản thành công! Bạn có thể đăng nhập ngay.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', error=error)
