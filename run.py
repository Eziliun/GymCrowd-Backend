from app import create_app
from app.algoritimo import pesquisar_no_google_maps

app = create_app()

pesquisar_no_google_maps()

if __name__ == "__main__":
    app.run(debug=True)