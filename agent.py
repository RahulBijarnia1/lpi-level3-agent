import subprocess
import json
import sys

query = sys.argv[1]

# ---- START LPI MCP SERVER ----
process = subprocess.Popen(
    ["node", "dist/src/index.js"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# ---- FUNCTION TO CALL TOOL ----
def call_tool(tool, input_data):
    try:
        request = {
            "tool": tool,
            "input": input_data
        }

        process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()

        response = process.stdout.readline()
        return json.loads(response)

    except Exception as e:
        return {"error": str(e)}

# ---- CALL LPI TOOLS (REAL MCP CALLS) ----
smile = call_tool("smile_overview", {})
knowledge = call_tool("query_knowledge", {"query": query})
cases = call_tool("get_case_studies", {"query": query})

# ---- COMBINE ----
combined = f"""
SMILE:
{smile}

KNOWLEDGE:
{knowledge}

CASE STUDIES:
{cases}
"""

# ---- OPTIONAL LLM ----
def call_llm(prompt):
    try:
        import requests
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        return res.json()["response"]
    except:
        return "LLM not running.\n" + prompt

final = call_llm(combined)

# ---- OUTPUT ----
print("\n--- SMILE OVERVIEW ---")
print(smile)

print("\n--- KNOWLEDGE ---")
print(knowledge)

print("\n--- CASE STUDIES ---")
print(cases)

print("\n--- FINAL ANSWER ---")
print(final)
