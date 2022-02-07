Running instructions:

* conda env create -f environment.yml
* conda activate weather
* redis-server
* cd weather
* Copy the weather/.env.example to weather/.env and replace the parameters with the real values.
* python manage runserver
* Access to http://127.0.0.1:8000/api?country=co&city=Bogota