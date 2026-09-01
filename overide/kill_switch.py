from typing import Optional


class SystemKillSwitch:
    """Emergency circuit breaker to halt autonomous trade execution."""

    def __init__(self, max_vix: float = 40.0, max_error_rate: float = 0.05) -> None:
        self.is_halted: bool = False
        self.halt_reason: Optional[str] = None
        self.max_vix: float = max_vix
        self.max_error_rate: float = max_error_rate

    def evaluate_system_health(self, current_vix: float, current_error_rate: float) -> bool:
        if current_vix > self.max_vix:
            self.trigger_halt(
                f"Market Volatility VIX ({current_vix}) exceeded safety threshold ({self.max_vix})."
            )
            return True

        if current_error_rate > self.max_error_rate:
            self.trigger_halt(
                f"Execution Error Rate ({current_error_rate:.2%}) exceeded limit ({self.max_error_rate:.2%})."
            )
            return True

        return self.is_halted

    def trigger_halt(self, reason: str) -> None:
        self.is_halted = True
        self.halt_reason = reason

    def reset(self) -> None:
        self.is_halted = False
        self.halt_reason = None