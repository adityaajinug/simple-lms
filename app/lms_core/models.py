import os
import sys
import csv
from django.contrib.auth.models import User
from lms_core.models import Course, CourseMember

# Set up Django environment
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 2)))  # Adjust the path to your project structure
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'
import django
django.setup()

# Define base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# File paths
user_data_path = os.path.join(base_dir, 'csv_data', 'user-data.csv')
course_data_path = os.path.join(base_dir, 'csv_data', 'course-data.csv')
member_data_path = os.path.join(base_dir, 'csv_data', 'member-data.csv')

# Import users
with open(user_data_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not User.objects.filter(username=row['username']).exists():
            User.objects.create_user(
                username=row['username'],
                password=row['password'],
                email=row['email']
            )

# Import courses
with open(course_data_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not Course.objects.filter(name=row['name']).exists():  # Use name to avoid conflicts
            try:
                teacher = User.objects.get(pk=int(row['teacher']))
                Course.objects.create(
                    name=row['name'],
                    description=row['description'],
                    price=row['price'],
                    teacher=teacher,
                    # Assuming you may have an image field; provide a default or skip if necessary
                    image=None  # Change to your logic to set the image if needed
                )
            except User.DoesNotExist:
                print(f"Teacher with ID {row['teacher']} not found. Skipping course creation.")

# Import course members
with open(member_data_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            course = Course.objects.get(pk=int(row['course_id']))
            user = User.objects.get(pk=int(row['user_id']))
            CourseMember.objects.create(
                course=course,
                user=user,
                roles=row['roles']  # Ensure roles are valid based on the defined choices
            )
        except (Course.DoesNotExist, User.DoesNotExist) as e:
            print(f"Error: {str(e)}. Skipping member creation.")
