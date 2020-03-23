import os, config, urllib.request, webbrowser
from sys import platform as _platform

# Import the Canvas class
from canvasapi import Canvas

# Canvas API URl
API_URL = config.API_URL

# Canvas API Key
API_KEY = config.CANVAS_TOKEN

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Grab course
COURSE_ID = config.COURSE_ID
course = canvas.get_course(COURSE_ID)

# Grab assignments
assignments = course.get_assignments(per_page=50)

# Clear CLI
os.system('cls')

assignmentList = {}
assignmentCounter = 1

# So Canvas API will automatically create a Paginated List whenever a call returns multiple objects.
# Apparently PaginatedList 'lazily loads' its elements, meaning we have no clue how any elements are in it
# without traversing the list fully. AKA no negative indexing with Python :(
for assignment in assignments:
    assignmentList[assignmentCounter] = assignment.id
    print(str(assignmentCounter) + ') ' + assignment.name + " date: " + assignment.due_at[0:10])
    assignmentCounter += 1

# Console input to select the assignment
print()
print('What assignment do you want to grade? (Enter #)')
assignment = int(input())

while assignment not in assignmentList:
    print('Not a valid option')
    print()
    print('What assignment do you want to grade? (Enter #)')
    assignment = int(input())
    print()

# Get selected assignment
toGrade = course.get_assignment(assignmentList[assignment])

# Create folder to place submissions
if not os.path.exists(toGrade.name):
    os.mkdir(toGrade.name)
print()

## Create a list variable in config.py with all your students (by canvas id), seperated by a comma
students = config.GRADING_SECTION

# Clear terminal
os.system('cls')

# Message for users
print('Downloading your grading section submissions...')

# Grab submissions and place in folder, will automatically give a zero to missing assignments
submissions = toGrade.get_submissions()
for submission in submissions:
    try:
        if submission.user_id in students:
            file = submission.attachments[0]['url']
            urllib.request.urlretrieve(file, './' + toGrade.name + '/' + submission.attachments[0]['filename'])
    except AttributeError:
        data = {
            comment: {
                text_comment: "No Submission."
            },
            submission: {
                posted_grade: 0
            }
        }
        print("Skipped " + str(submission.user))
        submission.edit(data)
        fake = int(input())

## Open SpeedGrader for specific assignment
webbrowser.open(config.SCHOOL_CANVAS+str(COURSE_ID)+'/gradebook/speed_grader?assignment_id='+str(toGrade.id))

# TAKE THIS OUT IF IT DOES NOT APPLY
## Open Rubrics for assignments (may be specific by course)
if "Lab" in toGrade.name:
    webbrowser.open(config.LAB_RUBRIC_URL)
elif "HW" in toGrade.name:
    webbrowser.open(config.HW_RUBRIC_URL)
else:
    webbrowser.open(config.GENERAL_URL)

# Opens the newly created folder with submissions
if _platform == "darwin":
    # macOS
    os.system('open ' + toGrade.name)
else:
    # Windows
    os.system('start ' + toGrade.name)

# Clear terminal and display finished message
os.system('cls')
print('Done!')