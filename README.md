# Django-Project

1. First Install Python3.9 standalone 
Link: https://www.python.org/downloads/release/python-3913/
2. Save the Python path in environment variable
   Ex: C:\Users\Your_UsernameAppData\Local\Programs\Python\Python39 (Windows)
3. Create a folder
4. Create a requirements.txt file and add below:
        Django==3.2
        firebase-admin
        pymongo
        django-crispy-forms
        crispy_bootstrap5
        djongo
        djangorestframework
5. Open commandline and go to the folder path and run:
     C:\Users\Your_Username\AppData\Local\Programs\Python\Python39\python -m venv env
     ./env/Scripts/activate
6.This is activate a virtual envirenment where we install all the dependencies
7. Type the command:
      pip install -r requirements.txt
8. Go inside the project path in commandlibe and run the command:
      python manage.py runserver
9. The developemnt server starts.

