from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class AdvisorOverride:
    override_id: str
    portfolio_id: str
    advisor_id: str
    original_trade: Dict[str, Any]
    modified_trade: Dict[str, Any]
    justification_category: str
    timestamp: datetime


class HumanOverrideEngine:
    """Captures and stores manual advisor overrides for retrospective audit."""

    def __init__(self) -> None:
        self.override_logs: List[AdvisorOverride] = []

    def record_override(self, override: AdvisorOverride) -> None:
        self.override_logs.append(override)

    def get_override_summary(self) -> Dict[str, Any]:
        total = len(self.override_logs)
        if total == 0:
            return {"total_overrides": 0, "categories": {}}

        categories: Dict[str, int] = {}
        for log in self.override_logs:
            categories[log.justification_category] = (
                categories.get(log.justification_category, 0) + 1
            )

        return {"total_overrides": total, "categories": categories}