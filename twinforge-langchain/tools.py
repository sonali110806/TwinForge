from langchain.tools import Tool

def restart_web():
    return "Web server restarted"

def scale_memory():
    return "Memory scaled"

def rate_limit():
    return "Rate limiting applied"

tools = [
    Tool(name="restart_web", func=restart_web, description="Fix CPU issue"),
    Tool(name="scale_memory", func=scale_memory, description="Increase memory"),
    Tool(name="rate_limit", func=rate_limit, description="Reduce traffic")
]
