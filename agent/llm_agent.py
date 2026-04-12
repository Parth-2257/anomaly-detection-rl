# LLM-based agent implementation

def get_llm_response(user_input):
    # handle list input (multi-turn)
    if isinstance(user_input, list):
        text = " | ".join(user_input).lower()
    else:
        text = user_input.lower()

    # simple rule-based detection (no API needed)
    attack_keywords = [
        "ignore", "disregard", "forget", "override",
        "bypass", "reveal", "password", "secret",
        "no restrictions", "pretend", "roleplay",
        "act as", "you are now", "dan"
    ]

    is_attack = any(keyword in text for keyword in attack_keywords)

    if is_attack:
        return {
            "is_attack": True,
            "type": "prompt_injection",
            "confidence": 0.9,
            "explanation": "Detected suspicious instruction pattern"
        }

    return {
        "is_attack": False,
        "type": "none",
        "confidence": 0.9,
        "explanation": "Input appears safe"
    }