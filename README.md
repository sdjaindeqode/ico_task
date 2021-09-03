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


## Accessing data through API
### Authentication of user
For registration of user:

    method: 'post'
    endpoint: '/auth/registration/'
    args: 'email', 'username', 'password1', 'password2'
    returns: 'key' (token that will be used for authentication)

For login of user:

    method: 'post'
    endpoint: '/auth/login/'
    args: 'username', 'password'
    returns: 'key' (token that will be used for authentication)
    
For logout of user:

    method: 'post'
    endpoint: '/auth/logout/'
    headers: 'Authorization : Token <your-token>'
    returns: 'detail'
    
### Working with other routes
For accessing token available for biddings:
    
    method: 'get'
    endpoint: '/api/v1/token/'
    returns: list of tokens available
    
For accessing specific token:
     
    method: 'get'
    endpoint: '/api/v1/token/<int:pk>'
    returns: token object
    
For creating new bid:
    
    method: 'post'
    endpoint: '/api/v1/bid/'
    headers: 'Authorization : Token <your-token>'
    data: 'token', 'number_of_token', 'bid_price'
    returns: token object
    
For accessing the bid:
    
    method: 'get'
    endpoint: '/api/v1/bid/<int:pk>'
    headers: 'Authorization : Token <your-token>'
    returns: token object

For updating the bid:
    
    method: 'put'
    endpoint: '/api/v1/bid/<int:pk>'
    headers: 'Authorization : Token <your-token>'
    data: 'number_of_token', 'bid_price'
    returns: token object


For deleting the bid:
    
    method: 'delete'
    endpoint: '/api/v1/bid/<int:pk>'
    headers: 'Authorization : Token <your-token>'
    returns: Empty response


For accessing successfull bid:
    
    method: 'get'
    endpoint: '/api/v1/bid/success'
    returns: list of successfull bids


For accessing failed bid:
    
    method: 'get'
    endpoint: '/api/v1/bid/failed'
    returns: list of failed bids