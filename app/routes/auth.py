from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

# ======================
# 🔹 LOGIN
# ======================
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            if user.is_admin:
                return redirect(url_for('notes.dashboard'))
            else:
                return redirect(url_for('notes.home'))
        else:
            flash("Username hoặc password không đúng!", "danger")

    return render_template('login.html')


# ======================
# 🔹 LOGOUT
# ======================
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Bạn đã đăng xuất thành công.", "success")
    return redirect(url_for('auth.login'))


# ======================
# 🔹 REGISTER
# ======================
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Kiểm tra username/email đã tồn tại
        if User.query.filter_by(username=username).first():
            flash("Username đã tồn tại! Vui lòng chọn tên khác.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Email đã tồn tại! Vui lòng dùng email khác.", "danger")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password, is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            flash("Tạo tài khoản thành công! Bạn có thể đăng nhập ngay.", "success")
            return redirect(url_for('auth.login'))

    return render_template('register.html')


# ======================
# 🔹 AJAX kiểm tra username tồn tại
# ======================
from flask import jsonify

@bp.route('/check_username', methods=['POST'])
def check_username():
    username = request.form.get('username', '').strip()
    exists = bool(User.query.filter_by(username=username).first())
    return jsonify({'exists': exists})
