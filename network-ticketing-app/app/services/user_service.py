from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User  # if needed for logging or future updates
from typing import Tuple, Optional, Dict

class UserService:
    @staticmethod
    def logout(user_id: int, db: Session) -> Tuple[Optional[Dict], Optional[str]]:
        try:
            err = UserRepository.mark_user_logged_out(user_id, db)
            if err:
                return None, err

            return {"message": "User logged out successfully"}, None
        except Exception as e:
            return None, str(e)
