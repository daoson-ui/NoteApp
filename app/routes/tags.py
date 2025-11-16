from flask import Blueprint, render_template, request, redirect, url_for, flash # type: ignore
from flask_login import login_required, current_user # type: ignore
from app import db
from app.models import Tag

# Blueprint quản lý Tags
tags_bp = Blueprint('tags', __name__, url_prefix='/admin/tags')


# ===========================
# List all tags
# ===========================
@tags_bp.route('/')
@login_required
def tag_list():
    if not getattr(current_user, "is_admin", False):
        return "Access denied", 403

    tags_data = Tag.query.order_by(Tag.id.asc()).all()

    return render_template('tag_list.html', tags=tags_data)


# ===========================
# Create new tag
# ===========================
@tags_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_tag():
    if not getattr(current_user, "is_admin", False):
        return "Access denied", 403

    if request.method == 'POST':
        name = request.form.get('name', '').strip()

        if not name:
            flash("Tag name cannot be empty", "danger")
            return redirect(url_for('tags.new_tag'))

        if Tag.query.filter_by(name=name).first():
            flash("Tag already exists!", "danger")
            return redirect(url_for('tags.new_tag'))

        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()

        flash("Tag created successfully!", "success")
        return redirect(url_for('tags.tag_list'))

    return render_template('tag_form.html', action="Create", tag=None)


# ===========================
# Edit tag
# ===========================
@tags_bp.route('/edit/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def edit_tag(tag_id):
    if not getattr(current_user, "is_admin", False):
        return "Access denied", 403

    tag = Tag.query.get_or_404(tag_id)

    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()

        if not new_name:
            flash("Tag name cannot be empty", "danger")
            return redirect(url_for('tags.edit_tag', tag_id=tag.id))

        if Tag.query.filter(Tag.name == new_name, Tag.id != tag.id).first():
            flash("Another tag with this name already exists!", "danger")
            return redirect(url_for('tags.edit_tag', tag_id=tag.id))

        tag.name = new_name
        db.session.commit()

        flash("Tag updated successfully!", "success")
        return redirect(url_for('tags.tag_list'))

    return render_template('tag_form.html', action="Edit", tag=tag)


# ===========================
# Delete tag
# ===========================
@tags_bp.route('/delete/<int:tag_id>', methods=['POST'])
@login_required
def delete_tag(tag_id):
    if not getattr(current_user, "is_admin", False):
        return "Access denied", 403

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash("Tag deleted successfully!", "success")
    return redirect(url_for('tags.tag_list'))
