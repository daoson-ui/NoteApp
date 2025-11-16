from flask import Blueprint, render_template, redirect, url_for, request, flash # type: ignore
from flask_login import login_required, current_user # type: ignore
from app import db
from app.models import User, Note, Tag

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# =============================
# CHECK QUYỀN ADMIN
# =============================
def admin_required():
    if not current_user.is_admin:
        flash("Bạn không có quyền truy cập trang này!")
        return False
    return True


# =============================
# TRANG DASHBOARD
# =============================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not admin_required():
        return redirect(url_for('notes.home'))

    users = User.query.all()

    # SORT ghi chú theo thời gian tạo mới nhất
    notes = Note.query.order_by(Note.created_at.desc()).all()

    tags = Tag.query.all()

    return render_template(
        'admin/dashboard.html',
        users=users,
        notes=notes,
        tags=tags
    )


# =============================
# QUẢN LÝ USER
# =============================
@admin_bp.route('/user/new', methods=['GET', 'POST'])
@login_required
def create_user():
    if not admin_required():
        return redirect(url_for('notes.home'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username đã tồn tại!")
            return redirect(url_for('admin.create_user'))

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Tạo user mới thành công!")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/user_form.html')


@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not admin_required():
        return redirect(url_for('notes.home'))

    user = User.query.get_or_404(user_id)

    if user.is_admin:
        flash("Không thể xóa tài khoản admin!")
        return redirect(url_for('admin.dashboard'))

    db.session.delete(user)
    db.session.commit()

    flash("Đã xóa user thành công!")
    return redirect(url_for('admin.dashboard'))


# =============================
# QUẢN LÝ TAG
# =============================
@admin_bp.route('/tag/new', methods=['GET', 'POST'])
@login_required
def create_tag():
    if not admin_required():
        return redirect(url_for('notes.home'))

    if request.method == 'POST':
        name = request.form['name']

        if Tag.query.filter_by(name=name).first():
            flash("Tag đã tồn tại!")
            return redirect(url_for('admin.create_tag'))

        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()

        flash("Thêm tag thành công!")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/tag_form.html')


@admin_bp.route('/tag/delete/<int:tag_id>', methods=['POST'])
@login_required
def delete_tag(tag_id):
    if not admin_required():
        return redirect(url_for('notes.home'))

    tag = Tag.query.get_or_404(tag_id)

    # Xóa mối liên kết trước
    for note in tag.notes:
        note.tags.remove(tag)

    db.session.delete(tag)
    db.session.commit()

    flash("Xóa tag thành công!")
    return redirect(url_for('admin.dashboard'))
