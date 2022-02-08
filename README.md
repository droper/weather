Running instructions:

* conda env create -f environment.yml
* conda activate weather
* conda install -c anaconda redis
* redis-server
* cd weather
* Copy the weather/.env.example to weather/.env and replace the parameters with the real values.
* cd ..
* python manage runserver
* With the browser go to http://127.0.0.1:8000/api?country=co&city=Bogota

* To run the tests: python manage.py test