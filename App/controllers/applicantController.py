from App.models import Applicant
from App.models import JobApplication
from App.models import JobListing
from App.database import db


def create_applicant(firstName, lastName, email, password):
    newuser = Applicant(firstName=firstName, lastName=lastName, email=email, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser


def apply_for_job(applicant_id, job_listing_id):
    # Check if the applicant exists
    applicant = Applicant.query.get(applicant_id)
    if applicant is None:
        print("Applicant does not exist!")
        return

    # Check if the job listing exists
    job_listing = JobListing.query.get(job_listing_id)
    if job_listing is None:
        print("Job listing does not exist!")
        return

    # Check if the applicant has already applied for this job
    existing_application = JobApplication.query.filter_by(applicantId=applicant_id, jobId=job_listing_id).first()
    if existing_application:
        print("This applicant has already applied for this job!")
        return

    # Create and add the new job application
    job_application = JobApplication(applicantId=applicant_id, jobId=job_listing_id)
    db.session.add(job_application)

    try:
        db.session.commit()  # Commit the new application to the database
        print(f"{applicant.firstName} applied for {job_listing.title}!")
    except Exception as e:
        db.session.rollback()  # Rollback if there's an error
        print(f"Error while applying for the job: {e}")

def view_jobs():
    """View all job listings."""
    job_listings = JobListing.query.all()
    for listing in job_listings:
        print(f"{listing.id}: {listing.title} - {listing.description}")

