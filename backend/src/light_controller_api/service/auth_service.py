from sqlalchemy import Boolean
from werkzeug.security import generate_password_hash
from backend.src.light_controller_api.repo.connection import get_session
from backend.src.light_controller_api.repo.auth_repo import UserRepository
from backend.src.light_controller_api.entity.logindatabase import User



class AuthService:

    def __init__(self, db_session=None):
        self.db = db_session or get_session()
        self.user_repo = UserRepository(self.db)



    # ---------------Register Service---------------
    def register(self, gmail_id: str, password: str) -> Boolean:
        existing_user = self.user_repo.find_by_gmail(gmail_id)
        if existing_user:
            raise ValueError("User already exists")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = self.user_repo.save(
            User(
                gmail_id=gmail_id,
                password=hashed_password
            )
        )

        if not user:
            return False
        return True



    #---------------Login Service---------------
    def login(self, gmail_id: str, password: str) -> Boolean:

        user_validate = self.user_repo.find_by_gmail_id_and_password(
            gmail_id,
            generate_password_hash(
                password,
                method='pbkdf2:sha256'
            )
        )

        if not user_validate:
            return False

        return True





