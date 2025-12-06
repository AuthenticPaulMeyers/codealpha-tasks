from flask import Flask
from .config import get_config
from .extensions import db, migrate
from datetime import timedelta

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    # Initialise Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import Blueprints here to avoid circular imports
    from .blueprints.api.routes import api_bp

    # Register Blueprints
    app.register_blueprint(api_bp)

    return app
