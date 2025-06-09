from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_required, LoginManager, current_user
from auth import login, logout, register
from models import Tickets, db, User
from os import path

# Initialise flask app
app = Flask(__name__)
app.secret_key = 'your_secret'

# SQLite Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'failure'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Route for homepage
@app.route('/')
def home():
    return render_template('home.html')

# Routes for authentication
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return login()

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return register()

@app.route('/logout')
def logout_page():
    return logout()

# Route for main page
@app.route('/main')
@login_required
def main():
    # Handles sorting paramters and sets default sorting
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    
    # Queries tickest based on sorting parameters
    if order == 'asc':
        tickets = Tickets.query.order_by(getattr(Tickets, sort_by).asc()).all()
    else:
        tickets = Tickets.query.order_by(getattr(Tickets, sort_by).desc()).all()
    
    columns = Tickets.__table__.columns.keys()
    return render_template('main.html',
                           tickets=tickets,
                           columns=columns,
                           selected_ticket=None,
                           active_tab='view',
                           sort_by=sort_by,
                           order=order)

# Route for creating new tickets
@app.route('/create', methods=['POST'])
@login_required
def create():
    try:
        if request.method == 'POST':
            # Get form data from request
            id = request.form.get('id')
            title = request.form.get('title')
            assigned_group = request.form.get('assigned_group')
            status = request.form.get('status')
            severity = request.form.get('severity')

            # Converts string to datetime object
            date_str = request.form.get('date')
            try:
                date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
            except:
                date = datetime.now()  # Defaults to the current time if conversion fails

            # Validate ticket ID and date
            id_exists = Tickets.query.filter_by(id=id).first()
            if id_exists:
                flash('That ticket ID already exists, try again!', category='failure')
            elif date > datetime.now():
                flash('Date cannot be in the future, try again!', category='failure')
            else:  
                # Create and save new ticket
                new_ticket = Tickets(
                    id=id,
                    title=title,
                    severity=severity,
                    status=status,
                    assigned_group=assigned_group,
                    date=date
                )
            
                db.session.add(new_ticket)
                db.session.commit()
                flash('Ticket created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occured: ' + str(e), category='failure')

    return redirect(url_for('main', _anchor='view'))

# Route to delete ticket (Admins only)
@app.route('/delete', methods=['POST'])
@login_required
def delete():
    id = request.form.get('id')
    ticket = Tickets.query.filter_by(id=id).first()

    if (current_user.admin == False):
        flash('You need admin permissions to delete a ticket', category='failure')
    elif (not ticket):
        flash('That is not a valid ticket ID, try again!', category='failure')
    else:
        try:
            db.session.delete(ticket)
            db.session.commit()
            flash('Ticket successfully deleted', category='success')
        except Exception as e:
            db.session.rollback()
            flash('An error occured: ' + str(e), category='failure')
    return redirect(url_for('main', _anchor='view'))

#Route for updating ticket information
@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    tickets = Tickets.query.all()
    columns = Tickets.__table__.columns.keys()
    selected_ticket = None
    
    if request.method == 'POST':
        if 'update_ticket' in request.form:
            ticket_id = request.form.get('id')
            ticket = Tickets.query.get(ticket_id)
            if ticket:
                try:
                    ticket.title = request.form.get('title')
                    ticket.severity = float(request.form.get('severity'))
                    ticket.status = request.form.get('status')
                    ticket.assigned_group = request.form.get('assigned_group')
                    
                    date_str = request.form.get('date')
                    if date_str:
                        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
                        if date > datetime.now():
                            flash('Date cannot be in the future', category='failure')
                            return render_template('main.html', 
                                                tickets=tickets,
                                                columns=columns,
                                                selected_ticket=ticket,
                                                active_tab='update')
                        else:
                            ticket.date = date
                            db.session.commit()
                            flash('Ticket updated successfully', category='success')
                            return render_template('main.html', 
                                                tickets=tickets,
                                                columns=columns,
                                                selected_ticket=None,
                                                active_tab='view')
                except Exception as e:
                    db.session.rollback()
                    flash('Failed to update ticket: ' + str(e), category='failure')
        else:
            ticket_id = request.form.get('id')
            selected_ticket = Tickets.query.get(ticket_id)
            if not selected_ticket:
                flash('That is not a valid ticket ID, try again!', category='failure')
    
    return render_template('main.html', 
                        tickets=tickets,
                        columns=columns,
                        selected_ticket=selected_ticket,
                        active_tab='view')

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

# Run the app
if __name__ == '__main__':
    create_database(app)
    app.run(debug=True)