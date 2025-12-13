import requests
from typing import Dict
from flask import jsonify
from typing import List, Optional
from sqlalchemy import Boolean
from backend.src.light_controller_api.repo.esp32_repo import Esp32Repository
from ..service.jwt_service import decode_jwt_token
from ..repo.auth_repo import UserRepository
from ..repo.connection import get_session


"""
THERE IS NO REPO LAYER FOR THIS ESP32 
THIS FILE TAKES TO ESP32 TO SET IT DEVICES USING ESP32_REPO / ESP32DATABASE
"""


#----------ESP32 Connection-----------
def _esp32_base_url(request) -> str:

    data = request.get_json()
    if not isinstance(data, Dict):
        return jsonify({"error": "Invalid data expected array of devices"}), 400


    token = request.cookies.get("access_token")
    gmail_id = decode_jwt_token(token)["gmail_id"]

    db = get_session()
    user_id = UserRepository(db).find_user_id_by_gmail_id(gmail_id)
    esp32_id = data.get("esp32_id")
    device = Esp32Repository(db).find_ip_port_by_user_id_and_device_id(user_id = user_id, device_id = esp32_id)
    ip, port = device.get("ip"), device.get("port")

    return f"http://{ip}:{port}"







def get_all_esp32(request) -> Optional[dict]:
    token = request.cookies.get("access_token")
    gmail_id = decode_jwt_token(token)["gmail_id"]

    db = get_session()
    user_id = UserRepository(db).find_user_id_by_gmail_id(gmail_id)
    return Esp32Repository(db).find_all_for_user(user_id)






def register_esp32(request) -> dict:
    device = request.get_json()

    token = request.cookies.get("access_token")
    gmail_id = decode_jwt_token(token)["gmail_id"]


    db = get_session()
    user_repo = UserRepository(db)
    esp32_repo = Esp32Repository(db)

    user_id = user_repo.find_user_id_by_gmail_id(gmail_id)
    esp32_id = esp32_repo.count_by_user_id(user_id)

    if not user_id:
        return {"status": "fail", "error": "User not found"}

    result = esp32_repo.create_device_for_user(
        user_id=user_id,
        name=device.get("name"),
        device_id=esp32_id + 1,
        ip_address=device.get("ip_address"),
        port=device.get("port")
    )

    if result:
        return {"status": "success"}

    return {"status": "fail"}



#-----------PUT SERVICE LAYER FOR ESP32 DEVICES-----------
def register_device_in_esp32(request) -> Optional[dict]:
    url = _esp32_base_url(request) + "/devices/register"
    request = requests.post(url, json=request.get_json(), timeout=3)
    request.raise_for_status()
    print(request.json())
    return request.json()



#-----------DELETE SERVICE LAYER FOR ESP32 DEVICES-----------
def delete_device_in_esp32(request) -> Optional[dict]:
    url = _esp32_base_url(request) + "/devices/delete"
    json_object = request.get_json()
    response = requests.post(url, json = json_object,timeout=3)
    response.raise_for_status()
    print(response.json())
    return response.json()


def delete_esp32_service(request) -> bool:
    data = request.get_json()
    token = request.cookies.get("access_token")
    gmail_id = decode_jwt_token(token)["gmail_id"]
    esp32_id = data.get("esp32_id")
    db = get_session()
    user_id = UserRepository(db).find_user_id_by_gmail_id(gmail_id)
    print(user_id, esp32_id)
    response = Esp32Repository(db).delete_esp32_by_user_id(user_id, esp32_id)
    return response




#-----------GETTER SERVICE LAYER FOR ESP32 DEVICES-----------
def get_devices(request) -> Optional[dict]:
    esp32_id = request.args.get("esp32_id", type=int)
    #device_id = request.args.get("device_id", type=int)

    token = request.cookies.get("access_token")
    gmail_id = decode_jwt_token(token)["gmail_id"]

    db = get_session()
    user_id = UserRepository(db).find_user_id_by_gmail_id(gmail_id)
    device = Esp32Repository(db).find_ip_port_by_user_id_and_device_id(user_id=user_id, device_id=esp32_id)
    ip, port = device.get("ip"), device.get("port")

    url = f"http://{ip}:{port}" + "/devices"
    request = requests.get(url, timeout=3)
    request.raise_for_status()
    return request.json()



#-----------GETTER SERVICE LAYER FOR ESP32 DEVICES-----------
def get_device(request) -> Optional[List[dict]]:

    esp32_id = request.args.get("esp32_id", type=int)
    device_id = request.args.get("device_id", type=int)

    token = request.cookies.get("access_token")
    gmail_id = decode_jwt_token(token)["gmail_id"]

    db = get_session()
    user_id = UserRepository(db).find_user_id_by_gmail_id(gmail_id)
    device = Esp32Repository(db).find_ip_port_by_user_id_and_device_id(user_id=user_id, device_id=esp32_id)
    ip, port = device.get("ip"), device.get("port")


    url = f"http://{ip}:{port}" +"/devices/get"
    json_object = {"device_id": device_id}
    request = requests.post(url, json = json_object, timeout=3)
    request.raise_for_status()
    return request.json()


#-----------SETTER SERVICE LAYER FOR ESP32 DEVICES-----------
def set_device(request) -> Boolean:
    url = _esp32_base_url(request) + "/devices/set"
    json_object = request.get_json()
    request = requests.post(url, json= json_object, timeout=3)
    request.raise_for_status()
    return request.json()



#-----------GETTER SERVICE LAYER FOR ESP32 DEVICES-----------
def get_availablity(request) -> Optional[dict]:
    esp32_id = request.args.get("esp32_id", type=int)

    token = request.cookies.get("access_token")
    gmail_id = decode_jwt_token(token)["gmail_id"]

    db = get_session()
    user_id = UserRepository(db).find_user_id_by_gmail_id(gmail_id)
    device = Esp32Repository(db).find_ip_port_by_user_id_and_device_id(user_id=user_id, device_id=esp32_id)
    ip, port = device.get("ip"), device.get("port")

    url = f"http://{ip}:{port}" + "/devices/available"
    request = requests.get(url, timeout=3)
    request.raise_for_status()
    return request.json()