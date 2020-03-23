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

# Get the course that the user is enrolled in as a TA
courses = canvas.get_courses(enrollment_role="TaEnrollment")

# Due to pagination, must print as a single index loop
for course in courses:
     print(str(course.id) + ": " + course.name)