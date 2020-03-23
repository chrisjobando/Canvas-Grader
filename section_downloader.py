import os, config, urllib.request, webbrowser

from sys import platform as _platform

# Import the Canvas class
from canvasapi import Canvas

# Canvas API URl
# https://SCHOOLNAME.instructure.com/api/v1/
API_URL = config.API_URL

# Canvas API Key
# To set it up, you need to create a token authorizing the app to access your Canvas courses:
# 1) In Canvas, select “Account” from the navigation bar on the left, then select “Settings” from the menu that pops out.
# 2) Scroll down to the “Approval Integrations:” section and click the “+ New Access Token” button. Fill in the popup (the “Purpose” field is just a note to yourself, so use something like “canvasrsync tool”, and the “Expires” field lets you put a limit on how long the token will be valid. I set it to the middle of the summer and re-generate a token every year).
# 3) Copy the token from the popup. Once you close the window, you cannot get the token again (you have to generate a new one).
# 4) Add token to config file as a variable
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

print()
print('What assignment do you want to grade? (Enter #)')
assignment = int(input())

while assignment not in assignmentList:
    print('Not a valid option')
    print()
    print('What assignment do you want to grade? (Enter #)')
    assignment = int(input())
    print()

toGrade = course.get_assignment(assignmentList[assignment])

if not os.path.exists(toGrade.name):
    os.mkdir(toGrade.name)

print()

## Create a list variable in config.py with all your students (by canvas id), seperated by a comma
students = config.GRADING_SECTION

os.system('cls')


print('Downloading your grading section submissions...')

# Grab submissions
submissions = toGrade.get_submissions()
for submission in submissions:
    try:
        if submission.user_id in students:
            file = submission.attachments[0]['url']
            urllib.request.urlretrieve(file, './' + toGrade.name + '/' + submission.attachments[0]['filename'])
    except AttributeError:
        data = {comment: {text_comment: "No Submission."}, submission: {posted_grade: 0}}
        print("Skipped " + str(submission.user))
        submission.edit(data)
        fake = int(input())

## Open SpeedGrader for specific assignment
webbrowser.open(config.SCHOOL_CANVAS+str(COURSE_ID)+'/gradebook/speed_grader?assignment_id='+str(toGrade.id))

## Open Rubrics for assignments (may be specific by course)
if "Lab" in toGrade.name:
    webbrowser.open(config.LAB_RUBRIC_URL)
elif "HW" in toGrade.name:
    webbrowser.open(config.HW_RUBRIC_URL)
else:
    webbrowser.open(config.GENERAL_URL)

if _platform == "darwin":
    # macOS
    os.system('open ' + toGrade.name)
else:
    # Windows
    os.system('start ' + toGrade.name)

os.system('cls')
print('Done!')