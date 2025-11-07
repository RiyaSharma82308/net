from sqlalchemy.orm import Session
from typing import Optional, Tuple
from app.models.refresh_token import RefreshToken

class TokenRepository:
    @staticmethod
    def store_refresh_token(user_id: int, token: str, db: Session) -> Tuple[Optional[RefreshToken], Optional[str]]:
        try:
            new_token = RefreshToken(user_id=user_id, token=token)
            db.add(new_token)
            db.commit()
            db.refresh(new_token)
            return new_token, None
        except Exception as e:
            return None, str(e)



    @staticmethod
    def delete_token(token: str, db: Session):
        try:
            record = db.query(RefreshToken).filter_by(token=token).first()
            if not record:
                return False, None
            db.delete(record)
            db.commit()
            return True, None
        except Exception as e:
            return False, str(e)



    def get_token(token: str, db: Session):
        try:
            record = db.query(RefreshToken).filter_by(token=token).first()
            return record, None
        except Exception as e:
            return None, str(e)