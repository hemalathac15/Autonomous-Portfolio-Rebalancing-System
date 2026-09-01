from datetime import datetime

class EscalationManager:
    """Handles escalation routing for flagged trades or compliance violations."""

    def __init__(self):
        self.escalation_queue = []

    def raise_escalation(self, portfolio_id: str, reason: str, severity: str = "HIGH") -> dict:
        ticket = {
            "ticket_id": f"ESC_{len(self.escalation_queue) + 1:04d}",
            "portfolio_id": portfolio_id,
            "reason": reason,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "OPEN_PENDING_REVIEW"
        }
        self.escalation_queue.append(ticket)
        return ticket

    def resolve_escalation(self, ticket_id: str, resolution_notes: str, reviewer_id: str) -> bool:
        for ticket in self.escalation_queue:
            if ticket["ticket_id"] == ticket_id:
                ticket["status"] = "RESOLVED"
                ticket["resolution_notes"] = resolution_notes
                ticket["reviewer_id"] = reviewer_id
                return True
        return False