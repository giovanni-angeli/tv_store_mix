
tv store server

__________________

```

```


### To run:

first time:

```
# export the path to the py virtualenv you created via 'make create_venv'
export PATH_TO_VENV=/opt/venvs/dj_mix
cd ./dj_mix/
(. $PATH_TO_VENV/bin/activate ; python ./web_app/manage.py makemigrations)
(. $PATH_TO_VENV/bin/activate ; python ./web_app/manage.py migrate)
(. $PATH_TO_VENV/bin/activate ; python ./web_app/manage.py createsuperuser)
(. $PATH_TO_VENV/bin/activate ; python ./web_app/manage.py runserver localhost:8008)
```

or simply:

```
(. /opt/venvs/dj_mix/bin/activate ; python  ./web_app/manage.py runserver localhost:8008)
```
