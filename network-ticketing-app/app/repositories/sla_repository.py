from app.models.sla import SLA

class SLARepository:
    @staticmethod
    def create(payload, db):
        try:
            sla = SLA(**payload.model_dump())
            db.add(sla)
            db.commit()
            db.refresh(sla)
            return sla, None
        except Exception as e:
            db.rollback()
            return None, str(e)

    @staticmethod
    def list_all(db):
        try:
            slas = db.query(SLA).all()
            return slas, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def update(sla_id, payload, db):
        try:
            sla = db.query(SLA).filter(SLA.sla_id == sla_id).first()
            if not sla:
                return None, "SLA not found"

            sla.severity = payload.severity
            sla.priority = payload.priority
            sla.time_limit_hr = payload.time_limit_hr
            db.commit()
            db.refresh(sla)
            return sla, None
        except Exception as e:
            db.rollback()
            return None, str(e)

    @staticmethod
    def delete(sla_id, db):
        try:
            sla = db.query(SLA).filter(SLA.sla_id == sla_id).first()
            if not sla:
                return None, "SLA not found"

            db.delete(sla)
            db.commit()
            return True, None
        except Exception as e:
            db.rollback()
            return None, str(e)
