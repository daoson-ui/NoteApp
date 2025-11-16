from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Tag

bp = Blueprint('tags', __name__)

# Xem tất cả tags (chỉ admin)
@bp.route('/tags')
@login_required
def tags_list():
    if not current_user.is_admin:
        return "Access denied", 403
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

# Tạo tag mới
@bp.route('/tag/new', methods=['GET', 'POST'])
@login_required
def new_tag():
    if not current_user.is_admin:
        return "Access denied", 403
    if request.method == 'POST':
        name = request.form['name']
        if Tag.query.filter_by(name=name).first():
            flash('Tag already exists!')
        else:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
            flash('Tag created!')
        return redirect(url_for('tags.tags_list'))
    return render_template('new_tag.html')

# Xóa tag
@bp.route('/tag/<int:tag_id>/delete', methods=['POST'])
@login_required
def delete_tag(tag_id):
    if not current_user.is_admin:
        return "Access denied", 403
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted!')
    return redirect(url_for('tags.tags_list'))

# Sửa tag
@bp.route('/tag/<int:tag_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tag(tag_id):
    if not current_user.is_admin:
        return "Access denied", 403
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        flash('Tag updated!')
        return redirect(url_for('tags.tags_list'))
    return render_template('edit_tag.html', tag=tag)
