from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    role = db.Column(db.String(40),nullable=False)
    email = db.Column(db.String(120),nullable=True)
    #username =  db.Column(db.String(20), nullable=False, unique=True   )
   # password = db.Column(db.String(120), nullable=False)

    courses = db.relationship('CourseStaff', back_populates='staff')

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

