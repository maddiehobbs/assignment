from models import User, Tickets
from werkzeug.security import check_password_hash

def test_user_model(init_database, app):
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user.username == 'testuser'
        assert check_password_hash(user.password, 'testpassword')
        assert not user.admin

def test_tickets_model(init_database, app):
    with app.app_context():
        ticket = Tickets.query.filter_by(id=1).first()
        assert ticket.title == 'Test Ticket'
        assert ticket.severity == 3.0
        assert ticket.status == 'Open'
        assert ticket.assigned_group == 'IT Support'