from __init__ import create_app

app = create_app()

# Default port:
if __name__ == '__main__':
    app.run()