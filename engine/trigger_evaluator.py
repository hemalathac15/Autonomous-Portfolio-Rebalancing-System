from datetime import datetime, timedelta
import numpy as np

class TriggerEvaluator:
    """Consolidates Threshold-based, Calendar-based, and Event-based rebalancing triggers."""

    def __init__(self, drift_threshold: float = 0.05, calendar_days: int = 90):
        self.drift_threshold = drift_threshold
        self.calendar_days = calendar_days

    def evaluate_triggers(
        self,
        max_drift: float,
        last_rebalance_date: datetime,
        market_shock_event: bool = False
    ) -> dict:
        days_since_rebalance = (datetime.utcnow() - last_rebalance_date).days

        threshold_trigger = max_drift >= self.drift_threshold
        calendar_trigger = days_since_rebalance >= self.calendar_days
        event_trigger = market_shock_event

        should_rebalance = threshold_trigger or calendar_trigger or event_trigger

        primary_reason = "NONE"
        if event_trigger:
            primary_reason = "EVENT_DRIVEN_MARKET_SHOCK"
        elif threshold_trigger:
            primary_reason = f"DRIFT_EXCEEDED_THRESHOLD ({max_drift:.2%})"
        elif calendar_trigger:
            primary_reason = f"CALENDAR_SCHEDULED ({days_since_rebalance} days)"

            return {
                "should_rebalance": should_rebalance,
                "primary_reason": primary_reason,
                "triggers_fired": {
                    "threshold": threshold_trigger,
                    "calendar": calendar_trigger,
                    "event": event_trigger
                }
            }