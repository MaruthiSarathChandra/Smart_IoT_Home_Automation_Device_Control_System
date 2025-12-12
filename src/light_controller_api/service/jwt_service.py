from flask import current_app, jsonify, request
import datetime, jwt

from sqlalchemy import Boolean


def create_jwt_token(gmail_id):
    payload = {
        "gmail_id": gmail_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    secret = current_app.config["JWT_SECRET"]

    return jwt.encode(payload, secret, algorithm='HS256')







def validate_jwt_token(request) -> Boolean:

    cookie_token = request.cookies.get("access_token")

    # Optional: If you also support Authorization Header (e.g., for an API client)
    if not cookie_token:
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            cookie_token = parts[1]  # Set token from header if cookie isn't found
        else:
            return False


    try:
        decoded = jwt.decode(cookie_token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
        if decoded:
            return True
    except Exception as e:
        print(e)
    return False





#---------------Decode Service---------------
def decode_jwt_token(token:str):

    if not token:
        return False

    try:
        decoded = (jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"]))
        return {
            "gmail_id": decoded["gmail_id"]
        }
    except Exception as e:
        return {"error": str(e)}



