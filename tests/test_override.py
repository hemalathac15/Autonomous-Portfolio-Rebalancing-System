# tests/test_override.py
import pytest
from overide import (
    EscalationManager,
    HumanOverrideEngine,
    InterventionClassifier,
    SystemKillSwitch,
)


def test_system_kill_switch():
    ks = SystemKillSwitch()
    assert ks is not None


def test_human_override_engine():
    engine = HumanOverrideEngine()
    assert engine is not None


def test_intervention_classifier():
    classifier = InterventionClassifier()
    assert classifier is not None


def test_escalation_manager():
    manager = EscalationManager()
    assert manager is not None