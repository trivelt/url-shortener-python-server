
# URL Shortener Server (Python DRF)

Simple URL shortener API written in Django Rest Framework. 
See also: [URL Shorteners Client (Haskell)](https://github.com/trivelt/url-shorteners-client)


## Installation and configuration

    git clone git@github.com:trivelt/url-shortener-python-server.git
    cd url-shortener-python-server
    virtualenv -p python3 venv && source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate

## Running
In order to run application, please execute:

    python3 manage.py runserver 

## Tests
You can run automated tests by executing the following command:

    python manage.py test

## API

- `POST /api/v1/link` - create a new short link. Required parameter: `long`, containing a valid URL to be shortened. 
 - `GET /api/v1/link` - return information (full long URL and short URL) about a link shortcut. Required parameter: `short`, containing a shortcut (for example: `2Bj`, not `http://localhost/2Bj`)
 - `GET /<shortcut>` - redirect to the full URL pointed by a shortcut 

You can interact with the API using `curl`, for example:
    
    $ curl -X POST -d 'long=http://polydev.pl' http://localhost:8000/api/v1/link
    {"long":"http://polydev.pl","short":"http://localhost:8000/2Bj"}
    
    $ curl -X GET http://localhost:8000/api/v1/link?short=2Bj
    {"long":"http://polydev.pl","short":"http://localhost:8000/2Bj"}
    
If you created a new short URL in a way showed above, you can type `http://localhost:8000/2Bj` in your browser - now you should be redirected to the specified long URL.  

