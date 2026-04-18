from langchain_ollama import OllamaLLM

# Create local LLM (make sure model is downloaded in Ollama)
llm = OllamaLLM(model="llama3")

def run_agent(input_text):
    response = llm.invoke(input_text)
    return response
