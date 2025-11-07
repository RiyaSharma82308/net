from app.repositories.sla_repository import SLARepository
from app.schemas.sla import SLAResponse
from datetime import datetime, timezone


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
    

    @staticmethod
    def filter_by_priority_severity(priority, severity, db):
        slas, err = SLARepository.filter_by_priority_severity(priority, severity, db)
        if err:
            return None, "Error filtering SLAs: " + err

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
    def get_sla_status_for_agent(db):
        tickets, err = SLARepository.get_tickets_with_sla_for_agent(db)
        if err:
            return None, "Error fetching tickets: " + err

        response = []
        now = datetime.now(timezone.utc)

        for t in tickets:
            if not t.due_date:
                continue

            created = t.created_at.replace(tzinfo=timezone.utc)
            due = t.due_date.replace(tzinfo=timezone.utc)

            total_sla = (due - created).total_seconds()
            remaining = (due - now).total_seconds()

            if remaining < 0:
                color = "red"
            else:
                pct = remaining / total_sla
                if pct > 0.4:
                    color = "green"
                elif pct > 0.1:
                    color = "yellow"
                else:
                    color = "red"

            response.append({
                "ticket_id": t.ticket_id,
                "issue_description": t.issue_description,
                "priority": t.priority.value if t.priority else None,
                "severity": t.severity.value if t.severity else None,
                "due_date": t.due_date.isoformat(),
                "remaining_seconds": max(int(remaining), 0),
                "sla_status_color": color
            })

        return response, None