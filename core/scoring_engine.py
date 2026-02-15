import json
from core.models import ConversationAnalysis


def compute_scores(signal_json: str) -> ConversationAnalysis:

    data = json.loads(signal_json)

    emotional = data.get("emotional_signals", [])
    behavioral = data.get("behavioral_signals", [])

    # ----------------------------
    # Attachment Inference (A)
    # ----------------------------
    anxious_score_a = 0
    avoidant_score_a = 0

    for sig in emotional:
        if sig.get("speaker") == "A":
            if sig.get("type") == "guilt induction":
                anxious_score_a += 1
            if sig.get("type") == "withdrawal":
                avoidant_score_a += 1

    if anxious_score_a > avoidant_score_a:
        attachment_a = "anxious"
    elif avoidant_score_a > anxious_score_a:
        attachment_a = "avoidant"
    else:
        attachment_a = data.get("attachment_a", "secure")

    # ----------------------------
    # Attachment Inference (B)
    # ----------------------------
    anxious_score_b = 0
    avoidant_score_b = 0

    for sig in emotional:
        if sig.get("speaker") == "B":
            if sig.get("type") == "guilt induction":
                anxious_score_b += 1
            if sig.get("type") == "withdrawal":
                avoidant_score_b += 1

    if anxious_score_b > avoidant_score_b:
        attachment_b = "anxious"
    elif avoidant_score_b > anxious_score_b:
        attachment_b = "avoidant"
    else:
        attachment_b = data.get("attachment_b", "secure")


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

    repair_attempts_a = 0
repair_attempts_b = 0

for sig in emotional:
    if sig["type"] == "repair attempt":
        if sig["speaker"] == "A":
            repair_attempts_a += 1
        else:
            repair_attempts_b += 1

total_repairs = repair_attempts_a + repair_attempts_b

if total_repairs > 0:
    emotional_labor_ratio = repair_attempts_a / total_repairs
else:
    emotional_labor_ratio = 0.5


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
