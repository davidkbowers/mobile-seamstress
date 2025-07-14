@echo off
echo Setting up Seamstress Management App...
echo.

echo Creating virtual environment...
python -m venv seamstress_env

echo Activating virtual environment...
call seamstress_env\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Setting up database...
python manage.py makemigrations
python manage.py migrate

echo.
echo Setup complete! 
echo.
echo Next steps:
echo 1. Create a superuser: python manage.py createsuperuser
echo 2. Start the server: python manage.py runserver
echo 3. Open http://127.0.0.1:8000/ in your browser
echo.
echo To activate the virtual environment later, run:
echo seamstress_env\Scripts\activate
echo.
pause
