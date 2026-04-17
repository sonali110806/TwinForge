print("🚀 TwinForge starting...")

from chroma_db.query import search_memory
from chroma_db.ingest import store_memory

print("✅ Imports successful")


def twinforge_ai(user_input):
    print("⚙️ Processing input...")

    memory = search_memory(user_input)
    context_text = " ".join(memory)

    print("🧠 Memory:", context_text)

    response = f"Based on memory: {context_text}"

    store_memory(user_input, id=hash(user_input))

    return response


print("🚀 TwinForge started! Type 'exit' to quit.\n")

while True:
    user_input = input("🧑 You: ")

    if user_input.lower() == "exit":
        break

    response = twinforge_ai(user_input)
    print("🤖 TwinForge:", response)