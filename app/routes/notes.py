from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Note, User, Tag
from datetime import datetime, timedelta

bp = Blueprint('notes', __name__)

# ==============================
# 🔹 HOME dành cho USER
# ==============================
@bp.route('/home')
@login_required
def home():
    notes_query = Note.query.filter_by(user_id=current_user.id)
    tags_all = Tag.query.all()
    selected_tag_id = request.args.get('tag', type=int)

    # Lấy tham số tìm kiếm
    q = request.args.get('q', '').strip()
    date_str = request.args.get('date', '').strip()

    if q:
        notes_query = notes_query.filter(
            (Note.title.ilike(f'%{q}%')) | (Note.content.ilike(f'%{q}%'))
        )

    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            notes_query = notes_query.filter(
                Note.created_at >= date_obj,
                Note.created_at < date_obj + timedelta(days=1)
            )
        except ValueError:
            flash("Ngày không hợp lệ!", "warning")

    if selected_tag_id:
        notes_query = notes_query.join(Note.tags).filter(Tag.id == selected_tag_id)

    notes = notes_query.order_by(Note.created_at.desc()).all()

    return render_template(
        'home.html',
        notes=notes,
        tags_all=tags_all,
        selected_tag_id=selected_tag_id,
        timedelta=timedelta
    )

# ==============================
# 🔹 DASHBOARD dành cho ADMIN
# ==============================
@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash("You are not allowed to access admin dashboard.", "danger")
        return redirect(url_for('notes.home'))

    users = User.query.all()
    notes_query = Note.query
    tags_all = Tag.query.all()
    selected_tag_id = request.args.get('tag', type=int)

    # Lấy tham số tìm kiếm
    q = request.args.get('q', '').strip()
    date_str = request.args.get('date', '').strip()

    if q:
        notes_query = notes_query.filter(
            (Note.title.ilike(f'%{q}%')) | (Note.content.ilike(f'%{q}%'))
        )

    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            notes_query = notes_query.filter(
                Note.created_at >= date_obj,
                Note.created_at < date_obj + timedelta(days=1)
            )
        except ValueError:
            flash("Ngày không hợp lệ!", "warning")

    if selected_tag_id:
        notes_query = notes_query.join(Note.tags).filter(Tag.id == selected_tag_id)

    notes = notes_query.order_by(Note.created_at.desc()).all()

    return render_template(
        'dashboard.html',
        users=users,
        notes=notes,
        tags_all=tags_all,
        selected_tag_id=selected_tag_id,
        timedelta=timedelta
    )

# ==============================
# 🔹 TẠO NOTE MỚI
# ==============================
@bp.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    tags = Tag.query.all()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        selected_tag_ids = request.form.getlist('tags')

        if not title:
            flash("Title cannot be empty!", "warning")
            return redirect(url_for('notes.new_note'))

        note = Note(title=title, content=content, user_id=current_user.id)

        for tag_id in selected_tag_ids:
            tag = Tag.query.get(int(tag_id))
            if tag:
                note.tags.append(tag)

        db.session.add(note)
        db.session.commit()
        flash("Note created successfully!", "success")
        return redirect(url_for('notes.dashboard' if current_user.is_admin else 'notes.home'))

    return render_template('new_note.html', note=None, tags=tags)

# ==============================
# 🔹 XEM NOTE
# ==============================
@bp.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id and not current_user.is_admin:
        flash("You do not have permission to view this note.", "danger")
        return redirect(url_for('notes.home'))
    return render_template('view_note.html', note=note, timedelta=timedelta)

# ==============================
# 🔹 CHỈNH SỬA NOTE (CHỈ NGƯỜI TẠO MỚI ĐƯỢC)
# ==============================
@bp.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    tags = Tag.query.all()
    if note.user_id != current_user.id:
        flash("You are not allowed to edit this note.", "danger")
        return redirect(url_for('notes.home') if not current_user.is_admin else url_for('notes.dashboard'))

    if request.method == 'POST':
        note.title = request.form.get('title', '').strip()
        note.content = request.form.get('content', '').strip()
        selected_tag_ids = request.form.getlist('tags')
        note.tags = []

        for tag_id in selected_tag_ids:
            tag = Tag.query.get(int(tag_id))
            if tag:
                note.tags.append(tag)

        db.session.commit()
        flash("Note updated!", "success")
        return redirect(url_for('notes.home'))

    return render_template('new_note.html', note=note, tags=tags)

# ==============================
# 🔹 XÓA NOTE (CHỈ NGƯỜI TẠO MỚI ĐƯỢC)
# ==============================
@bp.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("You cannot delete this note.", "danger")
        return redirect(url_for('notes.home') if not current_user.is_admin else url_for('notes.dashboard'))

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted successfully!", "success")
    return redirect(url_for('notes.home'))
