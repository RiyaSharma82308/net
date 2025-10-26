from app.repositories.sla_repository import SLARepository
from app.schemas.sla import SLAResponse

class SLAService:
    @staticmethod
    def create(payload, db):
        sla, err = SLARepository.create(payload, db)
        if err:
            return None, "Error creating SLA: " + err

        return SLAResponse(
            sla_id=sla.sla_id,
            severity=sla.severity.value,
            priority=sla.priority.value,
            time_limit_hr=sla.time_limit_hr
        ).dict(), None

    @staticmethod
    def list_all(db):
        slas, err = SLARepository.list_all(db)
        if err:
            return None, "Error fetching SLA list: " + err

        response = [
            SLAResponse(
                sla_id=s.sla_id,
                severity=s.severity.value,
                priority=s.priority.value,
                time_limit_hr=s.time_limit_hr
            ).dict()
            for s in slas
        ]

        return response, None

    @staticmethod
    def update(sla_id, payload, db):
        sla, err = SLARepository.update(sla_id, payload, db)
        if err:
            return None, "Error updating SLA: " + err

        return SLAResponse(
            sla_id=sla.sla_id,
            severity=sla.severity.value,
            priority=sla.priority.value,
            time_limit_hr=sla.time_limit_hr
        ).dict(), None

    @staticmethod
    def delete(sla_id, db):
        success, err = SLARepository.delete(sla_id, db)
        if err:
            return None, "Error deleting SLA: " + err

        return success, None
