from flask_login import current_user
from models import User

def test_register(client, init_database, app):
    with app.app_context():
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        }, follow_redirects=True)
        assert b'Account created successfully' in response.data
        assert User.query.filter_by(username='newuser').first() is not None

def test_login_logout(client, init_database, app):
    with app.test_client() as test_client:
        
        # Attempts to login user
        login_response = test_client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        
        assert b'logged in successfully' in login_response.data
        assert current_user.is_authenticated

        # Attempts to logout user
        logout_response = test_client.get('/auth/logout', follow_redirects=True)
        assert b'Logged out successfully' in logout_response.data
        
        # Make a new request to check authentication status
        response = test_client.get('/', follow_redirects=True)
        assert not current_user.is_authenticated

def test_login_invalid_credentials(client, init_database, app):
    with app.app_context():
        response = client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert b'Invalid username or password' in response.data