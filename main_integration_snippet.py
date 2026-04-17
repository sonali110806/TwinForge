# ─────────────────────────────────────────────────────────────────────────────
# HOW TO CONNECT chroma_db INTO YOUR main.py
# Add the lines below to your existing main.py
# ─────────────────────────────────────────────────────────────────────────────

from chroma_db.query import search_memory

# Example usage inside your AI pipeline:
user_input = "How do solar panels work?"

# 1. Retrieve relevant context from memory
context_docs = search_memory(user_input, n_results=2)
context = "\n".join(context_docs)

# 2. Feed context to your AI model (replace with your actual model call)
prompt = f"""You are TwinForge AI.
Use the following context to answer the user:

Context:
{context}

User: {user_input}
"""

# response = your_model.generate(prompt)  ← plug in your existing model here
print(prompt)