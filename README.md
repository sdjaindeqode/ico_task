# Initial Coin Offering

## Running the local environment

### Prerequisites:
1. `Redis` should be installed on system at port 6379.
2. `Postgresql` should be installed on system at port 5432.

### Run server
To run server run these commands:

    cd <path_to_ico_root>
    pip install -r requirements.txt
    python3 manage.py runserver

To run integration tests:

    python3 manage.py test


### Run Celery
To run celery run this commands:

    cd <path_to_ico_root>
    celery -A ico.celery worker --loglevel=info --beat



