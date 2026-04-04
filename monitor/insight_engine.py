from insight_engine import generate_insight
def generate_insight(cpu, memory):
    insight = {}

    # LOAD LEVEL
    if cpu > 80:
        insight["LOAD"] = "HIGH"
    elif cpu > 50:
        insight["LOAD"] = "MEDIUM"
    else:
        insight["LOAD"] = "LOW"

    # MEMORY STATE
    if memory > 1200:
        insight["MEMORY_STATE"] = "CRITICAL"
    elif memory > 900:
        insight["MEMORY_STATE"] = "ELEVATED"
    else:
        insight["MEMORY_STATE"] = "NORMAL"

    # SYSTEM STATE
    if cpu > 80 or memory > 1200:
        insight["STATE"] = "UNSTABLE"
    else:
        insight["STATE"] = "STABLE"
