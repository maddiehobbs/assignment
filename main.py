from datetime import datetime
from flask import Flask, render_template
from flask_login import login_required, LoginManager
from auth import login, logout, register
from models import Tickets, db, User
from os import path

app = Flask(__name__)
app.secret_key = 'your_secret'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#Login manager setup
login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return login()

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return register()

@app.route('/main')
@login_required
def main():
    tickets = Tickets.query.all()
    columns = Tickets.__table__.columns.keys()
    return render_template('main.html', 
                         tickets=tickets,
                         columns=columns)

@app.route('/logout')
def logout_page():
    return logout()

def create_database(app):
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

if __name__ == '__main__':
    create_database(app)
    app.run(debug=True)