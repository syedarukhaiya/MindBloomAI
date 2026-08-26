from app.services.safety_service import classify,RiskLevel
def test_normal(): assert classify("I had a busy day") == RiskLevel.NORMAL
def test_distress(): assert classify("I feel overwhelmed and cannot cope") == RiskLevel.DISTRESS
def test_high_risk(): assert classify("I want to kill myself") == RiskLevel.HIGH_RISK
