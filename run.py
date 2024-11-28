from app import create_app
from threading import Thread

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
