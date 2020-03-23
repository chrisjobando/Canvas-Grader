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

courses = canvas.get_courses(enrollment_role="TaEnrollment")

for course in courses:
     print(str(course.id) + ": " + course.name)