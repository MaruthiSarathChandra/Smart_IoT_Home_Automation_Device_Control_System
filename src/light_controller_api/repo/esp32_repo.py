from flask import current_app, jsonify
from typing import List, Optional
from sqlalchemy import Boolean
from sqlalchemy.orm import Session
from src.light_controller_api.entity.esp32database import Esp32Device


class Esp32Repository:
    def __init__(self, db: Session):
        self.db = db

    def create_device_for_user(
        self,
        user_id: int,
        name: str,
        device_id: int,
        ip_address: str,
        port: int
    ) -> bool:

        device = Esp32Device(
            user_id=user_id,
            name=name,
            device_id=device_id,
            ip_address=ip_address,
            port=port
        )

        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)

        return True


    def find_all_for_user(self, user_id: int):
        devices = self.db.query(Esp32Device).filter_by(user_id=user_id).all()

        return [
            {
                "esp32_id": d.device_id,
                "name": d.name,
                "ip_address": d.ip_address,
                "port": d.port
            }
            for d in devices
        ]


    def find_ip_port_by_user_id_and_device_id(self, user_id:int, device_id: int):
        device = (self.db.query(Esp32Device).filter_by(user_id=user_id, device_id=device_id).first())

        if device is None: return None

        return {
            "ip": device.ip_address,
            "port": device.port
        }

    def count_by_user_id(self, user_id: int) -> int:
        return self.db.query(Esp32Device).filter_by(user_id=user_id).count()

    def delete_esp32_by_user_id(self, user_id: int, esp32_id: int):
        try:
            rows_deleted = self.db.query(Esp32Device).filter_by(user_id=user_id, device_id=esp32_id).delete()
            self.db.commit()
            if rows_deleted > 0:
                return {"success": True}
            return {"success": False}
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}


