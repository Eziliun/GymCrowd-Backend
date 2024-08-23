import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    # Outros parâmetros de configuração (e.g., banco de dados)