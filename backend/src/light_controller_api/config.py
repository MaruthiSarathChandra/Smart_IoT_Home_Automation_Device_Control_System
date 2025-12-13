

class Config:
    DEBUG = True
    JWT_SECRET = "jwt_secret_456"


    # change these for your local MySQL
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_NAME = "miniproject4"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )




    # SECRET_KEY = "super_secret_123"
    #ESP32_API_ENDPOINT = "http://192.168.1.214"
    #ESP32_API_PORT = 0


