from App.database import db

class CourseStaff(db.Model):

    __tablename__ = 'coursestaff' 
    id = db.Column(db.Integer,primary_key=True)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable = True)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'),nullable = False)

    course = db.relationship('Course', back_populates='staff')
    staff = db.relationship('Staff', back_populates='courses')