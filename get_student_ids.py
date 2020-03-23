import os, config, urllib.request, webbrowser

from sys import platform as _platform

# Import the Canvas class
from canvasapi import Canvas

# Canvas API URl
# https://SCHOOLNAME.instructure.com/api/v1/
API_URL = config.API_URL

# Canvas API Key
API_KEY = config.CANVAS_TOKEN

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Grab course
COURSE_ID = config.COURSE_ID
course = canvas.get_course(COURSE_ID)

students = course.get_enrollments(per_page=50)

# Clear CLI
os.system('cls')

studentsPrinted = {}

for student in students:
    studentId = student.user["id"]
    if student.role == 'StudentEnrollment' and studentId not in studentsPrinted:
        studentName = student.user["name"]
        studentsPrinted[studentId] = 1;
        print(str(studentId) + ": " + studentName)