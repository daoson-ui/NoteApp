from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Note, User, Tag

bp = Blueprint('notes', __name__)

# Trang chính cho user
@bp.route('/home')
@login_required
def home():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', notes=notes, username=current_user.username)

# Dashboard cho admin
@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return "Access denied", 403
    users = User.query.all()
    notes = Note.query.all()
    return render_template('dashboard.html', users=users, notes=notes)

# Tạo note mới
@bp.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    tags = Tag.query.all()  # Lấy tất cả tag để hiển thị
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        selected_tag_ids = request.form.getlist('tags')  # Lấy list id các tag được chọn

        note = Note(title=title, content=content, user_id=current_user.id)
        
        # Gắn tag cho note
        for tag_id in selected_tag_ids:
            tag = Tag.query.get(int(tag_id))
            if tag:
                note.tags.append(tag)

        db.session.add(note)
        db.session.commit()
        flash('Note created!')
        
        if current_user.is_admin:
            return redirect(url_for('notes.dashboard'))
        else:
            return redirect(url_for('notes.home'))

    return render_template('new_note.html', note=None, tags=tags)

# Xem note
@bp.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id and not current_user.is_admin:
        return "Access denied", 403
    return render_template('view_note.html', note=note)

# Chỉnh sửa note
@bp.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    tags = Tag.query.all()
    if note.user_id != current_user.id and not current_user.is_admin:
        return "Access denied", 403
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']

        # Cập nhật tags
        selected_tag_ids = request.form.getlist('tags')
        note.tags = []  # Xóa tất cả tag cũ
        for tag_id in selected_tag_ids:
            tag = Tag.query.get(int(tag_id))
            if tag:
                note.tags.append(tag)

        db.session.commit()
        flash('Note updated!')

        if current_user.is_admin:
            return redirect(url_for('notes.dashboard'))
        else:
            return redirect(url_for('notes.home'))

    return render_template('new_note.html', note=note, tags=tags)

# Xóa note
@bp.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id and not current_user.is_admin:
        return "Access denied", 403

    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!')

    if current_user.is_admin:
        return redirect(url_for('notes.dashboard'))
    else:
        return redirect(url_for('notes.home'))
