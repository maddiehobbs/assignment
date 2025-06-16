import pytest
from models import User, Tickets

@pytest.fixture
def logged_in_user(client, init_database, app):
    with app.test_client() as test_client:
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()

            # Login user
            test_client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)
            return user

def test_main_page(client, logged_in_user, app):
    with app.test_client() as test_client:
        # Login user
        test_client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        
        # Make the request
        response = test_client.get('/tickets/main')
        assert b'Tickets R Us' in response.data
        assert b'Create Ticket' in response.data

def test_create_ticket(client, logged_in_user, app):
    with app.test_client() as test_client:
        # Login user
        test_client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        
        # Create ticket
        response = test_client.post('/tickets/create', data={
            'id': '2',
            'title': 'New Test Ticket',
            'severity': '2.5',
            'status': 'Open',
            'assigned_group': 'Customer Service',
            'date': '2023-06-01T10:00'
        }, follow_redirects=True)
        assert b'Ticket created successfully' in response.data
        with app.app_context():
            assert Tickets.query.filter_by(id=2).first() is not None

def test_delete_ticket(client, logged_in_user, init_database, app):
    with app.test_client() as test_client:
        # Login admin
        test_client.post('/auth/login', data={
            'username': 'adminuser',
            'password': 'adminpassword'
        }, follow_redirects=True)
        
        # Delete ticket
        response = test_client.post('/tickets/delete', data={
            'id': '1'
        }, follow_redirects=True)
        assert b'Ticket successfully deleted' in response.data
        with app.app_context():
            assert Tickets.query.filter_by(id=1).first() is None

def test_update_ticket(client, logged_in_user, app):
    with app.test_client() as test_client:
        # Login user
        test_client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        
        # Update ticket
        response = test_client.post('/tickets/update', data={
            'id': '1',
            'update_ticket': 'true',
            'title': 'Updated Test Ticket',
            'severity': '4.0',
            'status': 'In Progress',
            'assigned_group': 'Network Team',
            'date': '2023-06-02T11:00'
        }, follow_redirects=True)
        assert b'Ticket updated successfully' in response.data
        with app.app_context():
            updated_ticket = Tickets.query.filter_by(id=1).first()
            assert updated_ticket.title == 'Updated Test Ticket'
            assert updated_ticket.severity == 4.0