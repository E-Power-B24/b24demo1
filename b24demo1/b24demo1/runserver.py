from os import environ
from b24demo1 import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '4000'))
    except ValueError:
        PORT = 4000
    app.debug = True
    app.run(HOST, PORT)