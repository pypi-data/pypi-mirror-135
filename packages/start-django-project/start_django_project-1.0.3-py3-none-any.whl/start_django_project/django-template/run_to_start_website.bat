ECHO OFF
ECHO ============================================================
ECHO Starting Django Project
ECHO This script will make a new venv and install the requirements, then start the Django Project
ECHO it will stry to use 'python' command please make sure python is installed and the command to execute it is 'py -3.9'
ECHO This project is tested on Python 3.9. It may not work on other versions
ECHO If this script does not work, you will need to start django manually. This script is only a helper to make it easier to start the project.
ECHO Please follow the instructions in the README.txt file to start the project if you need to.
ECHO ============================================================

SET PYTHON=py -3.9
@REM Check what python to use from the path
@REM If we don't have python, we can't run the script

%PYTHON% --version
IF errorlevel 1 (
    ECHO Python 3.9 not found will try to use python from the path
    python --version

    IF NOT errorlevel 1 (
        ECHO "Python 3.9 not found in the path, trying to use the default python. If the default python is not 3.9. It is not gurnateed for the system to work properly"
        SET PYTHON=python
    ) ELSE (
        ECHO Python not found
        ECHO Please install python and make sure the command to execute it is 'py -3.9' or 'python'
        ECHO Exiting
        EXIT /B 1
    )
)

@REM Check if we have a venv
@REM If we do, activate it
@REM If we don't, create it


IF NOT EXIST venv\Scripts\activate.bat (
    ECHO Creating venv ... This may take a while
    %PYTHON% -m venv venv
)

@REM Install requirements if they are not already installed
@REM If they are, skip this step

IF NOT EXIST venv\req_installed  (
    ECHO Installing requirements
	"venv\Scripts\pip" install -r requirements.txt
    COPY NUL venv\req_installed
) ELSE (
    ECHO Requirements already installed
)

@REM Start Django

if EXIST manage.py (
    ECHO Making migrations
	"venv\Scripts\python" manage.py makemigrations

    ECHO Running migrations
	"venv\Scripts\python" manage.py migrate app
	"venv\Scripts\python" manage.py migrate

    ECHO Loading fixtures

    @REM LOOP through all fixtures in the fixtures folder in a for loop and load them one by one
    for %%f in (app\fixtures\*.*) do (
        ECHO Loading fixture %%f
        "venv\Scripts\python" manage.py loaddata %%f
    )

    IF NOT EXIST venv\user_created (
        ECHO ----------------------------------------------------------------------------------------------------
        ECHO ----------------------------------------------------------------------------------------------------
        ECHO Please create and admin user and password, you will need to use this to signin to the admin panel
        ECHO Please do not use a real password this is a development environment.
        ECHO Create an admin user

        COPY NUL venv\user_created
        "venv\Scripts\python" manage.py createsuperuser
    ) ELSE (
        ECHO Super User already created
    )

    ECHO Collecting static files
    "venv\Scripts\python" manage.py collectstatic --noinput

    ECHO Running server
    start "" /d iexplore.exe "http://localhost:8000"
	"venv\Scripts\python" manage.py runserver
)

PAUSE