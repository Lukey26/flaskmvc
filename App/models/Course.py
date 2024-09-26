from App.database import db

class Course(db.Model):
    __tablename__ = 'course' 

    id = db.Column(db.Integer,primary_key =True)
    course_name = db.Column(db.String(100),nullable=False,unique=True)
    
    staff = db.relationship('CourseStaff', back_populates='course')


