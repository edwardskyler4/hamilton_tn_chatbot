# Step-by-step code to:
# 1) Read the existing department-only intents JSON saved at /mnt/data/county_chatbot_intents.json
# 2) Add Spanish translations (simple template-based translations) for example_inputs and possible_responses
# 3) Save a bilingual JSON file
# 4) Save a CSV file (one row per intent; example inputs and responses pipe-separated)
# 5) Generate Rasa-compatible NLU training file (nlu.yml) with English and Spanish examples
# 6) Save all files and list their paths for download

import json, csv, os, textwrap
from pathlib import Path

# Paths
inpath = Path("/mnt/data/county_chatbot_intents.json")
bilingual_json_path = Path("/mnt/data/county_chatbot_intents_bilingual.json")
csv_path = Path("/mnt/data/county_chatbot_intents.csv")
rasa_nlu_path = Path("/mnt/data/nlu.yml")

# Load existing intents
with open(inpath, "r") as f:
    intents = json.load(f)

def translate_to_spanish_en_template(text, dept_name=None):
    """
    Very small template-based translator for typical patterns used in intents.
    Falls back to a generic Spanish phrasing if pattern not recognized.
    dept_name should be left as-is (English) unless a mapping is known.
    """
    t = text.lower()
    if "how do i contact" in t:
        return f"¿Cómo me comunico con {dept_name}?"
    if "what does the" in t and "do" in t:
        return f"¿Qué hace el {dept_name}?" if dept_name else "¿Qué hace este departamento?"
    if "hours" in t or "open" in t:
        return f"¿Cuál es el horario de atención del {dept_name}?" if dept_name else "¿Cuál es el horario de atención?"
    if "phone" in t or "contact" in t:
        return f"¿Cuál es el número de teléfono del {dept_name}?" if dept_name else "¿Cuál es el número de teléfono?"
    if "where is" in t or "address" in t:
        return f"¿Dónde está {dept_name}?" if dept_name else "¿Dónde está ubicado?"
    if "download" in t or "form" in t:
        return f"¿Dónde puedo descargar el formulario para {dept_name}?"
    if "pay" in t or "payment" in t:
        return f"¿Cómo puedo pagar en {dept_name}?"
    if "report" in t:
        return f"Quiero reportar un problema relacionado con {dept_name}."
    if "book appointment" in t or "schedule" in t:
        return f"Quisiera agendar una cita con {dept_name}."
    # Generic fallback
    return f"Consulta sobre {dept_name}" if dept_name else "Consulta sobre el departamento"

def translate_response_to_spanish_en_template(resp, dept_name=None):
    """
    Template-based translation for typical response templates.
    """
    r = resp.lower()
    # map common patterns
    if "you can contact" in r or "contact" in r:
        return f"Puede comunicarse con {dept_name} en..."
    if "is responsible for" in r or "responsible" in r:
        return f"El {dept_name} es responsable de..."
    if "office hours" in r or "hours" in r or "open during" in r:
        return f"El horario de atención del {dept_name} es..."
    if "here’s the contact information" in r or "here is the contact info" in r:
        return f"A continuación está la información de contacto del {dept_name}:"
    if "you can download" in r or "download that form" in r:
        return f"Puede descargar ese formulario aquí:"
    if "you can make payments" in r or "make payments online" in r:
        return f"Puede realizar pagos en línea aquí:"
    if "for emergencies call 911" in r:
        return "En caso de emergencia llame al 911."
    if "sure, i can connect" in r or "let me get someone" in r:
        return "Claro, puedo ponerlo en contacto con un representante del condado."
    # fallback
    return f"Respuesta del {dept_name}." if dept_name else "Respuesta del departamento."

# Build bilingual intents
bilingual_intents = []
for intent in intents:
    tag = intent.get("tag")
    # Derive a readable dept name from tag if it looks like a department tag
    # Many tags were created by lowercasing and replacing spaces with underscores in the initial file.
    # Try to reconstruct department name by replacing underscores and capitalizing words.
    dept_name = tag.replace("_", " ").title()
    # But if tag already was in nicer format, use intent text if provided; otherwise this is good.
    example_inputs_en = intent.get("example_inputs", [])
    responses_en = intent.get("possible_responses", [])
    # Generate Spanish translations using templates
    example_inputs_es = [translate_to_spanish_en_template(e, dept_name=dept_name) for e in example_inputs_en]
    responses_es = [translate_response_to_spanish_en_template(r, dept_name=dept_name) for r in responses_en]
    bilingual_intents.append({
        "tag": tag,
        "example_inputs": {"en": example_inputs_en, "es": example_inputs_es},
        "possible_responses": {"en": responses_en, "es": responses_es}
    })

# Save bilingual JSON
with open(bilingual_json_path, "w", encoding="utf-8") as f:
    json.dump(bilingual_intents, f, ensure_ascii=False, indent=2)

# Save CSV
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["tag", "example_inputs_en", "example_inputs_es", "possible_responses_en", "possible_responses_es"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in bilingual_intents:
        writer.writerow({
            "tag": item["tag"],
            "example_inputs_en": " | ".join(item["example_inputs"]["en"]),
            "example_inputs_es": " | ".join(item["example_inputs"]["es"]),
            "possible_responses_en": " | ".join(item["possible_responses"]["en"]),
            "possible_responses_es": " | ".join(item["possible_responses"]["es"])
        })

# Generate Rasa NLU training file (nlu.yml)
# We'll create intents with English and Spanish examples separated under the same intent name.
rasa_nlu_lines = [
    "version: \"3.1\"",
    "nlu:"
]

for item in bilingual_intents:
    tag = item["tag"]
    # English examples
    rasa_nlu_lines.append(f"- intent: {tag}_en")
    rasa_nlu_lines.append("  examples: |")
    for ex in item["example_inputs"]["en"]:
        rasa_nlu_lines.append(f"    - {ex}")
    # Spanish examples
    rasa_nlu_lines.append(f"- intent: {tag}_es")
    rasa_nlu_lines.append("  examples: |")
    for ex in item["example_inputs"]["es"]:
        rasa_nlu_lines.append(f"    - {ex}")

# Write to nlu.yml
with open(rasa_nlu_path, "w", encoding="utf-8") as f:
    f.write("\n".join(rasa_nlu_lines))

# Also create a simple "training pairs" CSV suitable for basic classifier training: columns intent, language, example
pairs_csv_path = Path("/mnt/data/county_chatbot_training_pairs.csv")
with open(pairs_csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["intent", "language", "example"])
    writer.writeheader()
    for item in bilingual_intents:
        tag = item["tag"]
        for ex in item["example_inputs"]["en"]:
            writer.writerow({"intent": tag, "language": "en", "example": ex})
        for ex in item["example_inputs"]["es"]:
            writer.writerow({"intent": tag, "language": "es", "example": ex})

# List created files
created_files = {
    "bilingual_json": str(bilingual_json_path),
    "csv": str(csv_path),
    "rasa_nlu": str(rasa_nlu_path),
    "training_pairs_csv": str(pairs_csv_path)
}

created_files

