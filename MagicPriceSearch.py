from app import app, db
from app.models import User, Card, Results, Site 

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Card': Card, 'Results': Results, 'Site': Site}
