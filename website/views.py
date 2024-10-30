from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='Static')

@main_bp.route('/')
def index():
    return render_template('index.html')