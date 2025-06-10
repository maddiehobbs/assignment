from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__)

# Route for homepage
@main_blueprint.route('/')
def home():
    return render_template('home.html')