from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # route login

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # register blueprints
    from app.routes.notes import bp as notes_bp
    app.register_blueprint(notes_bp)
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # route '/' redirect tới login hoặc dashboard/home
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for('notes.dashboard'))
            else:
                return redirect(url_for('notes.home'))
        return redirect(url_for('auth.login'))

    return app

# callback để Flask-Login load user
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
