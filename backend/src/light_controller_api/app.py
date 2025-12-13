from flask import Flask # creating a flask server
from flask import request, redirect

from backend.src.light_controller_api.repo.connection import init_db
from backend.src.light_controller_api.controller.auth import auth_bp
from config import Config
from backend.src.light_controller_api.service.jwt_service import validate_jwt_token
from backend.src.light_controller_api.controller.home_controller import home_bp
from backend.src.light_controller_api.controller.esp32_controller import esp32_bp






PUBLIC_ROUTES = [
    "/api/auth/login",
    "/api/auth/register",
    "/mobile/api/register",
    "/mobile/api/login"
]


def create_app():
    #creating app
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        init_db()

    #registering of blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(home_bp, url_prefix='/api/home')
    app.register_blueprint(esp32_bp, url_prefix="/api/esp32")


    @app.before_request
    def check_jwt_for_everything():
        path = request.path

        for public in PUBLIC_ROUTES:
            if path.startswith(public):
                return None

        decode = validate_jwt_token(request)
        if decode:
            request.user = request.cookies.get("access_token")
            return None

        return redirect("/api/auth/login")
    return app




#intailizing the server ipaddress
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000,debug=True)