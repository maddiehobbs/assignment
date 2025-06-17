import os
from models import Tickets, User, db

def test_home_page(client):
    response = client.get('/')
    assert b'Welcome to Tickets R Us!' in response.data

def test_create_database_existing(app):
    # Create an empty database file
    with open('instance/database.db', 'w') as f:
        pass
    
    with app.app_context():
        from main import create_database
        create_database(app)
        
        # Assert that no tickets were created
        tickets = Tickets.query.all()
        assert len(tickets) == 0
    
    # Cleanup
    if os.path.exists('instance/database.db'):
        os.remove('instance/database.db')

def test_load_user(app):
    with app.app_context():
        # Create a test user
        user = User(username='testuser', password='password')
        db.session.add(user)
        db.session.commit()
        
        login_manager = app.login_manager
        
        # Test the load_user function
        loaded_user = login_manager.user_callback(user.id)
        assert loaded_user is not None
        assert loaded_user.username == 'testuser'