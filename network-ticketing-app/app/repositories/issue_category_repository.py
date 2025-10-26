from app.models.issue_category import IssueCategory

class IssueCategoryRepository:
    @staticmethod
    def create(payload, db):
        try:
            category = IssueCategory(category_name=payload.category_name)
            db.add(category)
            db.commit()
            db.refresh(category)
            return category, None
        except Exception as e:
            db.rollback()
            return None, str(e)

    @staticmethod
    def list_all(db):
        try:
            categories = db.query(IssueCategory).all()
            return categories, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_by_name(name, db):
        try:
            category = db.query(IssueCategory).filter(IssueCategory.category_name == name).first()
            return category, None
        except Exception as e:
            return None, str(e)


    @staticmethod
    def update(category_id, payload, db):
        try:
            category = db.query(IssueCategory).filter(IssueCategory.category_id == category_id).first()
            if not category:
                return None, "Category not found"

            category.category_name = payload.category_name
            db.commit()
            db.refresh(category)
            return category, None
        except Exception as e:
            db.rollback()
            return None, str(e)

    @staticmethod
    def delete(category_id, db):
        try:
            category = db.query(IssueCategory).filter(IssueCategory.category_id == category_id).first()
            if not category:
                return None, "Category not found"

            db.delete(category)
            db.commit()
            return True, None
        except Exception as e:
            db.rollback()
            return None, str(e)
