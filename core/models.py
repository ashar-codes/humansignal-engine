from dataclasses import dataclass
from typing import List


@dataclass
class EmotionalSignal:
    speaker: str
    type: str  # validation, dismissal, guilt, blame, repair, escalation
    intensity: int  # 1–5


@dataclass
class BehavioralSignal:
    speaker: str
    category: str  # dominance, manipulation, withdrawal, dependency
    weight: int  # 1–5


@dataclass
class ConversationAnalysis:
    health_score: int
    emotional_safety: int
    risk_partner_a: int
    risk_partner_b: int
    attachment_a: str
    attachment_b: str
    power_imbalance: int
    manipulation_index: int
    emotional_labor_ratio: float
    volatility_score: int
