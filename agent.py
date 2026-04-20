import subprocess
import json
import sys

# ─── STEP 1: Call an LPI tool via MCP ───────────────────────────
def call_lpi_tool(tool_name, arguments={}):
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    result = subprocess.run(
        ["node", "../lpi-developer-kit/dist/src/index.js"],  # adjust path if needed
        input=json.dumps(request),
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

# ─── STEP 2: Get user question ──────────────────────────────────
question = sys.argv[1] if len(sys.argv) > 1 else "What is SMILE methodology?"

print(f"\n🤖 Agent received question: {question}\n")

# ─── STEP 3: Call LPI Tool 1 — smile_overview ───────────────────
print("📡 Calling LPI tool: smile_overview")
tool1_result = call_lpi_tool("smile_overview")
print(f"✅ Tool 1 result received\n")

# ─── STEP 4: Call LPI Tool 2 — query_knowledge ──────────────────
print("📡 Calling LPI tool: query_knowledge")
tool2_result = call_lpi_tool("query_knowledge", {"query": question})
print(f"✅ Tool 2 result received\n")

# ─── STEP 5: Combine and display answer with citations ──────────
print("=" * 50)
print("📋 ANSWER (with source citations):")
print("=" * 50)
print(f"\nBased on your question: '{question}'\n")
print("From [smile_overview]:")
print(json.dumps(tool1_result, indent=2)[:500])  # show first 500 chars
print("\nFrom [query_knowledge]:")
print(json.dumps(tool2_result, indent=2)[:500])
print("\n✅ Sources used: smile_overview, query_knowledge")
