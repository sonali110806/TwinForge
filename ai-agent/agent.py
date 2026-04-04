<<<<<<< HEAD
def get_prompt(issue, metrics):
    prompt = f"""
You are an AI DevOps Agent.

Analyze the system issue:
Issue: {issue}
Metrics: {metrics}

Tasks:
1. Identify root cause
2. Suggest exactly 3 fixes
3. Assign confidence (0 to 1)

Output format:
Root Cause:
Fix 1:
Fix 2:
Fix 3:
Confidence:
"""
    return prompt
=======
def build_prompt(issue: str, metrics: dict) -> str:
    """Build the LLM prompt for the AI DevOps agent."""
    return f"""You are an AI DevOps Agent operating a Digital Twin IT system.

System Issue: {issue}
Current Metrics: CPU={metrics.get('cpu')}%  Memory={metrics.get('memory')}%

Your task:
1. Identify the most likely root cause.
2. Propose exactly 3 remediation fixes ranked by safety.
3. Assign a confidence score (0.0-1.0) for your top fix.

Respond in this format:
Root Cause: <explanation>
Fix 1: <safest fix>
Fix 2: <medium-risk fix>
Fix 3: <aggressive fix>
Confidence: <0.0-1.0>
"""
>>>>>>> f456c65 (Initial TwinForge fullstack setup)
