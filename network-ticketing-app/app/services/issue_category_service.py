from app.repositories.issue_category_repository import IssueCategoryRepository

class IssueCategoryService:
    @staticmethod
    def create(payload, db):
        existing, err = IssueCategoryRepository.get_by_name(payload.category_name, db)
        if err:
            return None, err
        if existing:
            return None, "Category name already exists"

        category, err = IssueCategoryRepository.create(payload, db)
        if err:
            return None, err

        return {
            "category_id": category.category_id,
            "category_name": category.category_name
        }, None

    @staticmethod
    def list_all(db):
        categories, err = IssueCategoryRepository.list_all(db)
        if err:
            return None, err

        return [
            {
                "category_id": c.category_id,
                "category_name": c.category_name
            } for c in categories
        ], None

    @staticmethod
    def update(category_id, payload, db):
        existing, err = IssueCategoryRepository.get_by_name(payload.category_name, db)
        if err:
            return None, "Failed to check for duplicate category"

        if existing and existing.category_id != category_id:
            return None, "Another category with this name already exists"

        category, err = IssueCategoryRepository.update(category_id, payload, db)
        if err:
            return None, "Failed to update category"

        return {
            "category_id": category.category_id,
            "category_name": category.category_name
        }, None
    
    @staticmethod
    def delete(category_id, db):
        success, err = IssueCategoryRepository.delete(category_id, db)
        if err:
            return None, "Failed to delete category"
        return success, None