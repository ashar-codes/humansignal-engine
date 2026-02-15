import json
from core.models import ConversationAnalysis


def compute_scores(signal_json: str) -> ConversationAnalysis:

    data = json.loads(signal_json)

    emotional = data.get("emotional_signals", [])
    behavioral = data.get("behavioral_signals", [])

    risk_a = 0
    risk_b = 0
    manipulation = 0
    dominance = 0
    volatility = 0

    for sig in emotional:
        if sig["type"] in ["dismissal", "guilt induction", "blame shifting", "escalation"]:
            volatility += sig["intensity"]
            if sig["speaker"] == "A":
                risk_a += sig["intensity"]
            else:
                risk_b += sig["intensity"]

    for sig in behavioral:
        if sig["category"] == "manipulation":
            manipulation += sig["weight"]
        if sig["category"] == "dominance":
            dominance += sig["weight"]

    total_risk = risk_a + risk_b
    health = max(0, 100 - total_risk * 5)
    safety = max(0, 100 - volatility * 5)

    emotional_labor_ratio = 0.5  # placeholder (we improve later)

    return ConversationAnalysis(
        health_score=health,
        emotional_safety=safety,
        risk_partner_a=min(risk_a * 5, 100),
        risk_partner_b=min(risk_b * 5, 100),
        attachment_a=data.get("attachment_a", "unknown"),
        attachment_b=data.get("attachment_b", "unknown"),
        power_imbalance=min(dominance * 5, 100),
        manipulation_index=min(manipulation * 5, 100),
        emotional_labor_ratio=emotional_labor_ratio,
        volatility_score=min(volatility * 5, 100)
    )
