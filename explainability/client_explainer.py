class ClientExplainer:
    """Generates Grade-8 clear narratives for end clients."""

    @staticmethod
    def generate_narrative(portfolio_id: str, action_data: dict) -> str:
        if action_data["action"] == "HOLD":
            return f"Your portfolio ({portfolio_id}) is well on track! No action is needed today as your investments remain close to your personal financial goals."

        # Rebalance scenario
        trades = action_data["trades_required"]
        bought_assets = [idx for idx, val in enumerate(trades) if val > 0.01]
        sold_assets = [idx for idx, val in enumerate(trades) if val < -0.01]

        return (
            f"To keep your investment goal safe, we are rebalancing portfolio {portfolio_id}. "
            f"Due to recent market changes, we are trimming profits from overweight assets and "
            f"reinvesting into underweight categories to keep your risk at the right level."
        )