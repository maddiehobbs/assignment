from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from models import Tickets, db, User
from config import Config
from os import path
from werkzeug.security import generate_password_hash, check_password_hash

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
            add_sample_data()
            print("Database created!")


def add_sample_data():
    # Sample ticket data
    ticket_data = [
        {
            'id': 283, 'title': 'Network Outage', 'severity': 1.0,
            'status': 'Open', 'assigned_group': 'Network Team',
            'date': datetime.now()
        },
        {
            'id': 833, 'title': 'Printer Error', 'severity': 3.0,
            'status': 'In Progress', 'assigned_group': 'IT Support',
            'date': datetime.now()
        },
        {
            'id': 991, 'title': 'Email System Down', 'severity': 4.0,
            'status': 'Pending', 'assigned_group': 'System Admin',
            'date': datetime.now()
        },
        {
            'id': 264, 'title': 'Wrong Price Displayed', 'severity': 2.5,
            'status': 'Open', 'assigned_group': 'Prime Video',
            'date': datetime.now()
        },
        {
            'id': 112, 'title': 'Customer Unable to Subscribe to Channel', 'severity': 1.0,
            'status': 'Closed', 'assigned_group': 'Customer Service',
            'date': datetime.now()
        },
        {
            'id': 2889, 'title': 'Missing Cables', 'severity': 5.0,
            'status': 'Pending', 'assigned_group': 'Network Team',
            'date': datetime.now()
        },
        {
            'id': 21, 'title': 'Wrong Offer Shown', 'severity': 4.0,
            'status': 'In Progress', 'assigned_group': 'Customer Service',
            'date': datetime.now()
        },
        {
            'id': 37, 'title': 'Web Server is Down', 'severity': 1.0,
            'status': 'Open', 'assigned_group': 'Network Team',
            'date': datetime.now()
        },
        {
            'id': 555, 'title': 'Lost Package', 'severity': 4.5,
            'status': 'Pending', 'assigned_group': 'Customer Service',
            'date': datetime.now()
        },
        {
            'id': 91, 'title': 'Forgotten Password', 'severity': 4,
            'status': 'Closed', 'assigned_group': 'IT Support',
            'date': datetime.now()
        }
    ]

    user_data = [
        {'username': f'username{i}', 'password': generate_password_hash(f'password{i}', method='pbkdf2:sha256'), 'admin': False}
        for i in range(1, 10)
    ]

    # Add an admin user
    user_data.append(
        {
            'username': 'adminuser',
            'password': generate_password_hash('adminpassword1', method='pbkdf2:sha256'),
            'admin': True
        }
    )

    # Create and add User objects
    sample_users = [User(**user) for user in user_data]
    sample_tickets = [Tickets(**ticket) for ticket in ticket_data]

    db.session.add_all(sample_tickets)
    db.session.add_all(sample_users)
    db.session.commit()