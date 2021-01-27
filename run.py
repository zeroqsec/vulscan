from app import create_app


host  = '127.0.0.1'
port  = '8080'
debug = True
threaded = True

app = create_app()

if __name__ == '__main__':
    app.run(
        host = host,
        port = port,
        debug = debug,
        threaded = threaded
    )