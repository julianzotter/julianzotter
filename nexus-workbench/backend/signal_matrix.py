"""
NEXUS Signal Matrix — S = 0.35·R + 0.30·E + 0.20·C + 0.10·A − 0.05·U
"""
from dataclasses import dataclass

WEIGHTS = dict(R=0.35, E=0.30, C=0.20, A=0.10, U=-0.05)

SCOPE_PROFILES = {
    "HOLZBAU":    dict(R=.88, E=.85, C=.82, A=.79, U=.15),
    "BETONBAU":   dict(R=.92, E=.90, C=.88, A=.85, U=.10),
    "STAHLBAU":   dict(R=.85, E=.82, C=.78, A=.75, U=.18),
    "BIM":        dict(R=.80, E=.78, C=.75, A=.88, U=.12),
    "FERTIGTEIL": dict(R=.89, E=.86, C=.84, A=.81, U=.13),
    "KI-WERKZEUG":dict(R=.90, E=.75, C=.70, A=.95, U=.20),
    "ALLGEMEIN":  dict(R=.55, E=.55, C=.55, A=.55, U=.45),
}

RISK_THRESHOLDS = {"HIGH": 0.75, "MEDIUM": 0.55, "LOW": 0.0}


@dataclass
class SignalResult:
    scope: str
    R: float; E: float; C: float; A: float; U: float
    score: float
    risk: str


def compute(scope: str, overrides: dict | None = None) -> SignalResult:
    sig = {**SCOPE_PROFILES.get(scope, SCOPE_PROFILES["ALLGEMEIN"]), **(overrides or {})}
    score = sum(WEIGHTS[k] * sig[k] for k in WEIGHTS)
    risk = next(r for r, t in RISK_THRESHOLDS.items() if score >= t)
    return SignalResult(scope=scope, score=round(score, 4), risk=risk, **sig)


def detect_scope(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["holz","gl24","gl28","c24","c16","ec5","brettschicht","kerto","clt","bsp"]):
        return "HOLZBAU"
    if any(k in t for k in ["beton","stahlbeton","c30","c40","c25","ec2","durchstanz"]):
        return "BETONBAU"
    if any(k in t for k in ["stahl","s355","s275","ipe","hea","heb","ec3"]):
        return "STAHLBAU"
    if any(k in t for k in ["ifc","bim","revit","allplan","speckle","glTF"]):
        return "BIM"
    if any(k in t for k in ["fertigteil","precast","elementdecke","doppelwand"]):
        return "FERTIGTEIL"
    if any(k in t for k in ["ki","llm","agent","gpt","claude","deepseek","rag","embedding"]):
        return "KI-WERKZEUG"
    return "ALLGEMEIN"
