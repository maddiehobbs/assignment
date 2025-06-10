from datetime import datetime
from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask_login import login_required, current_user
from models import Tickets, db

tickets_blueprint = Blueprint('tickets', __name__)

# Route for main page
@tickets_blueprint.route('/main')
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
@tickets_blueprint.route('/create', methods=['POST'])
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

    return redirect(url_for('tickets.main', _anchor='view'))

# Route to delete ticket (Admins only)
@tickets_blueprint.route('/delete', methods=['POST'])
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
    return redirect(url_for('tickets.main', _anchor='view'))

#Route for updating ticket information
@tickets_blueprint.route('/update', methods=['GET', 'POST'])
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