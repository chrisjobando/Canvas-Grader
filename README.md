# Canvas Grader

## Instructions

1. Create a file called config.py to add your environmental variables
2. Add your canvas token:
   - To set it up, you need to create a token authorizing the app to access your Canvas courses:
   1. In Canvas, select “Account” from the navigation bar on the left, then select “Settings” from the menu that pops out.
   2. Scroll down to the “Approval Integrations:” section and click the “+ New Access Token” button. Fill in the popup (the “Purpose” field is just a note to yourself, so use something like “canvasrsync tool”, and the “Expires” field lets you put a limit on how long the token will be valid. I set it to the middle of the summer and re-generate a token every year).
   3. Copy the token from the popup. Once you close the window, you cannot get the token again (you have to generate a new one).
   4. Add token to config file as a variable called `CANVAS_TOKEN`
3. Add your api url to config.py as `API_URL`
   - For GT, it is "https://gatech.instructure.com/api/v1/"
4. Similarly, add your school's canvas url to config.py as `SCHOOL_CANVAS`
   - For GT, it is "https://gatech.instructure.com/courses/"
5. To run a script, use `py [filename].py`
   - I recommend running `py get_course_id.py` -> `py get_student_ids.py` -> `py section_downloader.py`
