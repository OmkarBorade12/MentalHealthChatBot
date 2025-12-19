import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database Configuration
    # Pattern: mysql+pymysql://user:password@host/db_name
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', 'Jumbo@1234')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_name = os.environ.get('DB_NAME', 'mental_health_bot')
    
    # URL encode password to handle special chars like '@'
    from urllib.parse import quote_plus
    encoded_password = quote_plus(db_password)
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}"
            
    SQLALCHEMY_TRACK_MODIFICATIONS = False
