from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["metric"],
    template="Anomaly detected: {metric}"
)
