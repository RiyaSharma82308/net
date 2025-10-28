from app.repositories.address_repository import AddressRepository
from app.schemas.address import (
    AddressCreateWithUserId,
    AddressCreateInternal,
    AddressUpdate
)
from datetime import datetime

class AddressService:
    @staticmethod
    def create_for_user(payload: AddressCreateWithUserId, db):
        if not payload.user_id:
            return None, "User ID is required to create an address"

        missing_fields = [
            field for field in ["street", "city", "state", "postal_code", "country"]
            if not getattr(payload, field, None)
        ]
        if missing_fields:
            return None, f"Missing required fields: {', '.join(missing_fields)}"

        address, err = AddressRepository.create(payload, db)
        if err:
            if "foreign key" in err.lower():
                return None, "Invalid user ID — user does not exist"
            return None, f"Database error: {err}"

        return AddressService._format_address(address)

    @staticmethod
    def create_for_self(payload: AddressCreateInternal, db):
        if not payload.user_id:
            return None, "User ID is required to create an address"

        address, err = AddressRepository.create(payload, db)
        if err:
            if "foreign key" in err.lower():
                return None, "Invalid user ID — user does not exist"
            return None, f"Failed to create address: {err}"

        return AddressService._format_address(address)

    @staticmethod
    def list_by_user(user_id: int, db):
        addresses, err = AddressRepository.list_by_user(user_id, db)
        if err:
            return None, f"Failed to fetch addresses: {err}"

        formatted = [AddressService._format_address_dict(a) for a in addresses]
        return formatted, None


    @staticmethod
    def update(address_id: int, payload: AddressUpdate, db):
        address, err = AddressRepository.update(address_id, payload, db)
        if err:
            if "not found" in err.lower():
                return None, "Address not found"
            return None, f"Failed to update address: {err}"

        if not address:
            return None, "No address returned after update"

        return AddressService._format_address(address)
        


    @staticmethod
    def delete(address_id: int, db):
        success, err = AddressRepository.delete(address_id, db)
        if err:
            if "not found" in err.lower():
                return None, "Address not found"
            return None, f"Failed to delete address: {err}"
        return success, None

    @staticmethod
    def _format_address(address):
        return {
            "address_id": address.address_id,
            "user_id": address.user_id,
            "street": address.street,
            "city": address.city,
            "state": address.state,
            "postal_code": address.postal_code,
            "country": address.country,
            "created_at": address.created_at.isoformat() if address.created_at else None
        }, None  # ✅ consistent (response, error)

    @staticmethod
    def _format_address_dict(address):
        return {
            "address_id": address.address_id,
            "user_id": address.user_id,
            "street": address.street,
            "city": address.city,
            "state": address.state,
            "postal_code": address.postal_code,
            "country": address.country,
            "created_at": address.created_at.isoformat() if address.created_at else None
        }
    
    @staticmethod
    def get_by_id(address_id: int, db):
        address, err = AddressRepository.get_by_id(address_id, db)
        if err or not address:
            return None, "Address not found"
        return AddressService._format_address_dict(address), None

