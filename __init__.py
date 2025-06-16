from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from models import Tickets, db, User
from config import Config
from os import path

login_manager = LoginManager()

def create_app(test_config=None):
    # Initialise flask app
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.update(test_config)

    # Flask-Login configuration
    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'failure'
    login_manager.init_app(app)

    # Register blueprints
    from blueprints.auth.routes import auth_blueprint
    from blueprints.tickets.routes import tickets_blueprint
    from blueprints.main.routes import main_blueprint
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(tickets_blueprint, url_prefix='/tickets')
    app.register_blueprint(main_blueprint)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Create tables for testing
    if test_config and test_config.get('TESTING'):
        with app.app_context():
            db.create_all()
    
    return app

# Database initilisation
def create_database(app):
    # Creates database if it does not exist
    if not path.exists('instance/' + 'database.db'):
        with app.app_context():
            db.create_all()

            # Sample tickets
            sample_tickets = [
                Tickets(
                    id=283,
                    title='Network Outage',
                    severity=1.0,
                    status='Open',
                    assigned_group='Network Team',
                    date=datetime.now()
                ),
                Tickets(
                    id=833,
                    title='Printer Error',
                    severity=3.0,
                    status='In Progress',
                    assigned_group='IT Support',
                    date=datetime.now()

                ),
                Tickets(
                    id=991,
                    title='Email System Down',
                    severity=4.0,
                    status='Pending',
                    assigned_group='System Admin',
                    date=datetime.now()
                ),
                Tickets(
                    id=263,
                    title='Wrong Price Displayed',
                    severity=2.5,
                    status='Open',
                    assigned_group='Prime Video',
                    date=datetime.now()
                ),
                Tickets(
                    id=112,
                    title='Customer Unable to Subscribe to Channel',
                    severity=1,
                    status='Closed',
                    assigned_group='Customer Service',
                    date=datetime.now()
                )
            ]

            db.session.add_all(sample_tickets)
            db.session.commit()

            print("Database created!")