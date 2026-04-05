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
