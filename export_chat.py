import json

log_path = "/home/luca/.gemini/antigravity-cli/brain/0e734859-4349-45a7-aba8-5ef03739bd06/.system_generated/logs/transcript.jsonl"
out_path = "/home/luca/Scrivania/Storico_Conversazione.txt"

with open(log_path, "r", encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
    fout.write("========================================================================\n")
    fout.write("                  STORICO CONVERSAZIONE AGENTE                          \n")
    fout.write("========================================================================\n\n")
    for line in fin:
        if not line.strip(): continue
        try:
            entry = json.loads(line)
            role = entry.get("source", "")
            step_type = entry.get("type", "")
            content = entry.get("content", "")
            
            if step_type == "USER_INPUT":
                fout.write(f"\n[UTENTE] --------------------------------------------------------\n{content}\n")
            elif role == "MODEL" and step_type == "PLANNER_RESPONSE":
                fout.write(f"\n[AI] ------------------------------------------------------------\n{content}\n")
        except:
            pass
