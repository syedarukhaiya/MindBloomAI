import re
from enum import StrEnum
class RiskLevel(StrEnum): NORMAL="NORMAL"; DISTRESS="DISTRESS"; HIGH_RISK="HIGH_RISK"
HIGH_PATTERNS=[r"\bkill myself\b",r"\bsuicide\b",r"\bwant to die\b",r"\bend my life\b",r"\bself[- ]?harm\b",r"\bhurt myself\b",r"\bno reason to live\b"]
DISTRESS_PATTERNS=[r"\boverwhelmed\b",r"\bhopeless\b",r"\bcan.?t cope\b",r"\bpanic\b",r"\bworthless\b",r"\bvery alone\b",r"\bburned out\b"]
def classify(text:str)->RiskLevel:
 t=text.lower()
 if any(re.search(p,t) for p in HIGH_PATTERNS): return RiskLevel.HIGH_RISK
 if any(re.search(p,t) for p in DISTRESS_PATTERNS): return RiskLevel.DISTRESS
 return RiskLevel.NORMAL
def escalation_message()->str:
 return "What you're describing sounds serious, and you deserve support from a real person right now. Please move toward someone you trust or a qualified professional, and use verified emergency/crisis resources available in your location if you may be in immediate danger."
