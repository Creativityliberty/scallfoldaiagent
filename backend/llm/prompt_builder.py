from typing import Dict

def build_rrla_prompt(context: Dict) -> str:
    intent = context.get("intent", "")
    task_type = context.get("task_type", "")
    clean_input = context.get("clean_input", "")
    return (
        f"Tu es un agent de raisonnement. Décompose cette requête en étapes logiques.\n\n"
        f"Requête: {clean_input}\n"
        f"Type de tâche: {task_type}\n"
        f"Intention: {intent}\n\n"
        "Réponds en JSON avec cette structure:\n"
        "{\n    \"steps\": [\n        {\"id\": 1, \"action\": \"...\", \"rationale\": \"...\"},\n"
        "        {\"id\": 2, \"action\": \"...\", \"rationale\": \"...\"}\n    ]\n}"
    )
