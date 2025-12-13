from sqlalchemy import Boolean
from sqlalchemy.orm import Session
from backend.src.light_controller_api.entity.logindatabase import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_gmail(self, gmail_id: str) -> Boolean:

        query = self.db.query(User).filter(User.gmail_id == gmail_id).first()
        if not query:
            return False
        return True

    def find_by_gmail_id_and_password(self, gmail_id: str, password: str) -> Boolean:

        query = self.db.query(User).filter(User.gmail_id == gmail_id and password == password).first()
        if not query:
            return False
        return True

    def find_user_id_by_gmail_id(self, gmail_id: str):
        user = self.db.query(User).filter_by(gmail_id=gmail_id).first()
        return user.id if user else None


    def save(self, user: User) -> Boolean:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        if not User:
            return False
        return True


    def delete(self, user: User) -> Boolean:
        self.db.delete(user)

        if self.db.commit(): return True
        return False

