import json

# Systemprompt für alle Requests
SYSTEM_PROMPT = (
    "Du bist ein Modell, das nur auf Basis der gegebenen Aussagen argumentiert. "
    "Wenn Informationen fehlen, sagst du klar, dass du es nicht wissen kannst. "
    "Du halluzinierst keine zusätzlichen Fakten."
)


def build_user_prompt(question: str, text_a: str, text_b: str) -> str:
    """
    Baut den User-Prompt für eine Instanz (Frage + Aussage A + B + Instruktionen).
    """
    return f"""Du bekommst zwei Aussagen zu einem Thema.
Thema / Frage: "{question}"

Aussage A:
\"\"\"{text_a}\"\"\"

Aussage B:
\"\"\"{text_b}\"\"\"

Aufgabe:
1. Erkenne, ob sich A und B logisch widersprechen.
2. Erkläre den Konflikt in 1–3 Sätzen.
3. Entscheide NICHT, welche Aussage wahr ist, wenn diese Information nicht eindeutig aus A und B hervorgeht.
4. Nutze KEIN externes Weltwissen – bewerte nur die beiden Aussagen.

Gib deine Antwort NUR als JSON-Objekt mit den Feldern:
- contradiction: "yes" oder "no"
- explanation: string
- can_decide_truth: "yes" oder "no"
- chosen_side: "A", "B" oder "none"
- choice_reason: string
"""


# JSON-Schema für strukturierte Ausgabe (Ollama "format"-Feld)
FORMAT_SCHEMA = {
    "type": "object",
    "properties": {
        "contradiction": {
            "type": "string",
            "enum": ["yes", "no"]
        },
        "explanation": {
            "type": "string"
        },
        "can_decide_truth": {
            "type": "string",
            "enum": ["yes", "no"]
        },
        "chosen_side": {
            "type": "string",
            "enum": ["A", "B", "none"]
        },
        "choice_reason": {
            "type": "string"
        }
    },
    "required": [
        "contradiction",
        "explanation",
        "can_decide_truth",
        "chosen_side",
        "choice_reason"
    ]
}
