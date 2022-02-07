Running instructions:

* conda env create -f environment.yml
* conda activate weather
* redis-server
* cd weather
* python manage runserver
* Access to http://127.0.0.1:8000/api?country=co&city=Bogota