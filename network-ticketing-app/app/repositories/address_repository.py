from app.models.address import Address

class AddressRepository:
    @staticmethod
    def create(payload, db):
        try:
            address = Address(**payload.model_dump())
            db.add(address)
            db.commit()
            db.refresh(address)
            return address, None
        except Exception as e:
            db.rollback()
            print("❌ Address creation error:", e)
            return None, str(e)

    @staticmethod
    def list_by_user(user_id, db):
        try:
            addresses = db.query(Address).filter(Address.user_id == user_id).all()
            return addresses, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_by_id(address_id, db):
        try:
            address = db.query(Address).filter(Address.address_id == address_id).first()
            return address, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def update(address_id, payload, db):
        try:
            address = db.query(Address).filter(Address.address_id == address_id).first()
            if not address:
                return None, "Address not found"

            for field, value in payload.model_dump().items():
                setattr(address, field, value)

            db.commit()
            db.refresh(address)
            return address, None
        except Exception as e:
            db.rollback()
            return None, str(e)

    @staticmethod
    def delete(address_id, db):
        try:
            address = db.query(Address).filter(Address.address_id == address_id).first()
            if not address:
                return None, "Address not found"

            db.delete(address)
            db.commit()
            return True, None
        except Exception as e:
            db.rollback()
            return None, str(e)
