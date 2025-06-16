from flask_login import LoginManager
import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash
from models import Tickets, db, User
from main import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Create a test user
        user = User(
            username='testuser',
            password=generate_password_hash('testpassword', method='pbkdf2:sha256'),
            admin=False
        )
        db.session.add(user)
        
        # Create a test admin user
        admin = User(
            username='adminuser', 
            password=generate_password_hash('adminpassword', method='pbkdf2:sha256'), 
            admin=True
        )
        db.session.add(admin)
        
        # Create a test ticket
        ticket = Tickets(
            id=1, 
            title='Test Ticket', 
            severity=3.0, 
            status='Open', 
            assigned_group='IT Support', 
            date=datetime.now()
        )
        db.session.add(ticket)
        db.session.commit()

    yield db

    with app.app_context():
        db.drop_all()