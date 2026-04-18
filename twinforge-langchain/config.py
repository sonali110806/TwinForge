import os
from langchain_openai import ChatOpenAI

# Add your API key
os.environ["OPENAI_API_KEY"] = "your_api_key_here"

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
