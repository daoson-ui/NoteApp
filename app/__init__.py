from flask import Flask, redirect, url_for # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import LoginManager, current_user # type: ignore
from flask_migrate import Migrate # type: ignore
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'   # Trang login chính


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Khởi tạo extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # -----------------------------
    # Đăng ký các BLUEPRINT
    # -----------------------------
    from app.routes.notes import bp as notes_bp
    app.register_blueprint(notes_bp)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # Blueprint quản lý Tags
    from app.routes.tags import tags_bp
    app.register_blueprint(tags_bp)

    # -----------------------------
    # Route gốc '/'
    # -----------------------------
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if getattr(current_user, "is_admin", False):
                return redirect(url_for('notes.dashboard'))
            return redirect(url_for('notes.home'))
        return redirect(url_for('auth.login'))

    return app


# Load user cho Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
