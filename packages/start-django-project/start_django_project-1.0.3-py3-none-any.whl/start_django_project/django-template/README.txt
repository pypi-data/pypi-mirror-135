Instructions to start django:

You should try running the included batch file to start django. However, if it fails, you can start it from the command line.
Command line skills are required.

Note: "py -3.9" executes python 3.9 if you have it installed with the python launcher.
      If not replace it with "python" or whatevery command you use to start python.

Execute all the scripts inside the project folder:

1. Create a virtual environment
    py -3.9 -m venv ./venv

2. Activate the virtual environment
    ./venv/script/activate

3. Install requirements
    pip install -r requirements.txt

4. Run migrations, one at a time:
    python manage.py makemigrations
    python manage.py migrate app
    python manage.py migrate

5. Create superuser
    python manage.py createsuperuser

6. Start the server
    python manage.py runserver

7. Copy the link from the command line and paste it into your browser