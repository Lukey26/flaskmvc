import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, create_applicant, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("firstName", default="rob")
@click.argument("lastName", default="man")
@click.argument("email", default="rob@email.com")
@click.argument("password", default="robpass")
def create_user_command(username, email, password):
    create_user(username, email, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
applicant commands
'''
applicant_cli = AppGroup('applicant', help='Applicant object commands')
@applicant_cli.command("create", help="creates an applicant")
@click.argument("username", default="unemployed")
@click.argument("email", default="unemployed@email.com")
@click.argument("password", default="robpass")
def create_applicant_command(username, email, password):
    create_applicant(username, email, password)
    print(f'{username} created!')

app.cli.add_command(applicant_cli) # add the group to the cli

'''
admin commands
'''
admin_cli = AppGroup('admin', help='Applicant object commands')
@applicant_cli.command("create", help="creates an applicant")
@click.argument("username", default="unemployed")
@click.argument("email", default="unemployed@email.com")
@click.argument("password", default="robpass")
def create_applicant_command(username, email, password):
    create_applicant(username, email, password)
    print(f'{username} created!')

app.cli.add_command(applicant_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)