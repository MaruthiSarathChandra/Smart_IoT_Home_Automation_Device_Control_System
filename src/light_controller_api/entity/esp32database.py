from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.light_controller_api.repo.connection import Base
from src.light_controller_api.entity.logindatabase import Base



class Esp32Device(Base):
    __tablename__ = 'esp32_devices'

    id = Column(Integer, primary_key=True, autoincrement=True)

    #foreign key
    user_id = Column(Integer, ForeignKey('usersdb.id'), nullable=False)

    #----------Device naming----------
    name = Column(String(45), nullable=False)
    device_id = Column(Integer, nullable=False)

    #----------Device communication data----------
    ip_address = Column(String(45), nullable=False)
    port = Column(Integer, nullable=False)

    #----------Status----------
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Esp32Device id={self.id} user_id={self.user_id} ip={self.ip_address}>"


