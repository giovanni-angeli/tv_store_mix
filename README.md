
tv store server

__________________


## set up:

```
# set the path for your virtualenv
export PATH_TO_VENV=/opt/venvs/dj_mix

(virtualenv -p python3 $PATH_TO_VENV)
(. $PATH_TO_VENV/bin/activate ; pip install --upgrade pip ; pip install wheel)

# cd into the path of your clone of the repo
cd ./tv_store_mix/

(. $PATH_TO_VENV/bin/activate ; python ./web_app/manage.py makemigrations)
(. $PATH_TO_VENV/bin/activate ; python ./web_app/manage.py migrate)
(. $PATH_TO_VENV/bin/activate ; python ./web_app/manage.py createsuperuser)
(. $PATH_TO_VENV/bin/activate ; python ./web_app/manage.py runserver localhost:8008)
```

## to run:

```
(. /opt/venvs/dj_mix/bin/activate ; python  ./web_app/manage.py runserver localhost:8008)
```
