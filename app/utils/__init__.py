import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure database
    database_url = os.environ.get("DATABASE_URL")
    
    # Fix the URL if necessary for SQLAlchemy
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # Set default SQLite path if DATABASE_URL is not set
    if not database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(app.instance_path, 'qreactor.sqlite')
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Ensure upload folder exists
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Setup login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Context processor to inject variables into all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # Register blueprints
    from app.routes.auth import auth as auth_blueprint
    from app.routes.main import main as main_blueprint
    from app.routes.user import user as user_blueprint
    from app.routes.admin import admin as admin_blueprint
    from app.routes.qr import qr as qr_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(qr_blueprint)

    # Shell context for Flask CLI
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'app': app}

    return app # This file is intentionally left empty to mark the directory as a Python package. 
