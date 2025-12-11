
import re

UNSAFE_PATTERNS = [
    r"ignore all previous instructions",
    r"pretend you are",
    r"do anything now",
    r"DAN",
    r"jailbreak",
    r"bypass",
    r"disable safety",
    r"roleplay",
    r"tell me all the passwords"

]


def extract_info(text):
    result = {
        "label": None,
        "confidence_score":None,
        "explanation":None
    }

    label_match = re.search(r'"?label"?\s*:\s*(\d+)', text, re.IGNORECASE)
    if label_match:
        result["label"] = int(label_match.group(1))

    #score_match = re.search(r'"?score"?\s*:\s*([\d.]+)', text, re.IGNORECASE)
    #if score_match:
    #    result["score"] = float(score_match.group(1))

    confidence_score = re.search(r'"?confidence_score"?\s*:\s*"?([^",\}]+)"?', text, re.IGNORECASE)
    if confidence_score:
        result["confidence_score"] = float(confidence_score.group(1))

    explanation_match = re.search(r'"?explanation"?\s*:\s*"([^"]+)"', text, re.IGNORECASE)
    if explanation_match:
        result["explanation"] = explanation_match.group(1)
    return result


def rule_based_check(prompt: str) -> float:
    """Return a rule-based unsafe score (0-1)."""
    for pat in UNSAFE_PATTERNS:
        if re.search(pat, prompt, re.IGNORECASE):
            return 0.8  # high unsafe risk
    return 0.2  # mostly safe