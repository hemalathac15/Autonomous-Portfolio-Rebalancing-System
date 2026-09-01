# tests/test_data.py
import pytest
from data import (
    AssetUniverse,
    ClientConstraintProfile,
    ConstraintEngine,
    SyntheticPortfolioGenerator,
)


def test_client_constraint_profile():
    # Pass required positional argument 'portfolio_id'
    profile = ClientConstraintProfile("P_101")
    assert profile is not None


def test_constraint_engine():
    engine = ConstraintEngine()
    assert engine is not None


def test_synthetic_portfolio_generator():
    generator = SyntheticPortfolioGenerator()
    assert generator is not None