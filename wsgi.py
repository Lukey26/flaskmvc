from flask import cli
import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models.Course import Course
from App.models.Staff import Staff
from App.models.CourseStaff import CourseStaff
from App.main import create_app
from App.controllers import (create_user, get_all_users_json, get_all_users, initialize)

# Create the Flask app
app = create_app()
migrate = get_migrate(app)

# Initialize the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('Database initialized')


'''
Staff and Course Commands
'''

# Group for organizing staff-related commands
staff_cli = AppGroup('staff', help='Staff object commands')

# Add staff command
@staff_cli.command('add')
#@click.argument('id')
@click.argument('username')
@click.argument('role')
def add_staff(username, role):
    """Add a new staff member."""
    staff = Staff(name=username, role=role)
    db.session.add(staff)
    db.session.commit()
    print(f"Added staff: {staff.name}, Role: {staff.role}")

@staff_cli.command('delete')
@click.argument('username',default = 'bob')
def delete_staff(username):
    bob = Staff.query.filter_by(name=username).first()
    if not bob:
        print(f'{username} not found')
        return
    db.session.delete(bob)
    db.session.commit()
    print(f'{username} deleted')
# Group for organizing course-related commands
course_cli = AppGroup('course', help='Course object commands')

# Add course command
@course_cli.command('add')
#@click.argument('id')
@click.argument('course_name')
def add_course(course_name):
    """Add a new course."""
    course = Course(course_name=course_name)
    db.session.add(course)
    db.session.commit()
    print(f"Added course: {course.course_name}")

# Command to link staff and course
@course_cli.command('link-staff')
@click.argument('staff_id', type=int)
@click.argument('course_id', type=int)
def link_staff_course(staff_id, course_id):
    """Link staff to a course."""
    link = CourseStaff(staff_id=staff_id, course_id=course_id)
    db.session.add(link)
    db.session.commit()
    print(f"Linked staff ID: {staff_id} to course ID: {course_id}")

# Print all data command
@course_cli.command('print-data')
def print_data():
    """Print all staff and courses."""
    staff_members = Staff.query.all()
    courses = Course.query.all()

    print("Staff Members:")
    for staff in staff_members:
        print(f"ID: {staff.id}, Username: {staff.name}, Role: {staff.role}")

    print("\nCourses:")
    for course in courses:
        print(f"ID: {course.id}, Course Name: {course.course_name}")

    print("\nCourse Staff Links:")
    course_staff_links = CourseStaff.query.all()
    for link in course_staff_links:
        print(f"Staff ID: {link.staff_id} is linked to Course ID: {link.course_id}")


'''
User Commands
'''

# Group for organizing user-related commands
user_cli = AppGroup('user', help='User object commands')

# Create user command
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# List users command
@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

# Register the user group commands
app.cli.add_command(user_cli)


'''
Test Commands
'''

# Group for organizing test-related commands
test_cli = AppGroup('test', help='Testing commands')

# Run user tests
@test_cli.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

# Register the test group commands
app.cli.add_command(test_cli)

# Register the staff and course group commands
app.cli.add_command(staff_cli)
app.cli.add_command(course_cli)

if __name__ == "__main__":
    app.run()
