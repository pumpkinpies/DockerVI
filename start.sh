python manage.py makemigrations
python manage.py migrate
nohup python test.py &

python manage.py runserver 0.0.0.0:8000
