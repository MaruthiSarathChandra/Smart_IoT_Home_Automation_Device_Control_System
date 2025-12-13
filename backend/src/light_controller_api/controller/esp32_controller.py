from flask import jsonify, Blueprint, request
from backend.src.light_controller_api.service.esp32_service import set_device, get_device, get_devices, register_device_in_esp32, delete_esp32_service, delete_device_in_esp32, get_availablity, register_esp32, get_all_esp32

esp32_bp = Blueprint('esp32_bp', __name__)
#esp32_url = current_app.config['ESP32_API_ENDPOINT']




#-----------SETTER FOR ESP32 DEVICES-----------
@esp32_bp.route("/put/device", methods=["POST"])
def set_esp32_device():

    """
    {
        1. jwt_token
        2. esp32_id
        2. device_id
        3. data_value
    }
    :return:
    """

    try:
        return jsonify(set_device(request)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502





#-----------GETTER FOR ESP32 DEVICES-----------
@esp32_bp.route("/get/device", methods=["GET"])
def get_esp32_device():
    """
    {
        1. jwt_token
        2. esp32_id
        3. device_id
    }
    :return:
    """
    try:
        return get_device(request)
    except Exception as e:
        return jsonify({"error": str(e)}), 502




@esp32_bp.route("/register_esp32/device", methods=["POST"])
def register_device():
    """
    {
        1. jwt_token
        2. esp32_id
        3. device_id
        4. name
        5. is_read
    }
    :return:
    """

    try:
        return register_device_in_esp32(request)
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@esp32_bp.route("/delete/device", methods=["DELETE"])
def delete_device():
    """
    {
        1. jwt_token
        2. esp32_id
        3. device_id
    }

    :return:
    """

    try:
        return jsonify(delete_device_in_esp32(request)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502



@esp32_bp.route("/get/devices", methods=["GET"])
def get_esp32_devices():
    try:
        return jsonify(get_devices(request)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502




@esp32_bp.route("/available", methods=["GET"])
def get_esp32_availablity():
    try:
        return jsonify(get_availablity(request)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502




@esp32_bp.route("/get/esp32", methods=["GET"])
def get_esp32():
    try:
        return jsonify(get_all_esp32(request)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502





@esp32_bp.route("/register/device", methods=["POST"])
def register_esp32_device():

    try:
        #print(request.json())
        return jsonify(register_esp32(request)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 502



@esp32_bp.route("/esp32/delete", methods=["POST"])
def delete_esp32_device():

    try:
        return jsonify(delete_esp32_service(request)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502
