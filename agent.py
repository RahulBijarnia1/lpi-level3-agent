import requests
import sys

query = sys.argv[1]

# ---- TOOL FUNCTIONS ----
def smile_overview():
    return "SMILE methodology focuses on structured explainability."

def query_knowledge(q):
    return f"Knowledge about '{q}': Used in modern systems."

def get_case_studies(q):
    return f"Case study: '{q}' used in healthcare and finance."

# ---- CALL TOOLS ----
smile = smile_overview()
knowledge = query_knowledge(query)
cases = get_case_studies(query)

# ---- COMBINE ----
combined = f"""
SMILE:
{smile}

KNOWLEDGE:
{knowledge}

CASE STUDIES:
{cases}
"""

# ---- CALL LLM ----
def call_llm(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        return res.json()["response"]
    except:
        return "LLM not running. Showing raw output:\n" + prompt

final = call_llm(combined)

# ---- PRINT OUTPUT ----
print("\n--- SMILE OVERVIEW ---")
print(smile)

print("\n--- KNOWLEDGE ---")
print(knowledge)

print("\n--- CASE STUDIES ---")
print(cases)

print("\n--- FINAL ANSWER ---")
print(final)