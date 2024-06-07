# machine_production_log
setup Python -version ==3.9
conda create -n envname python==3.9 
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
 
