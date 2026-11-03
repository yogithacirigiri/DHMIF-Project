from llm import LLM


llm = LLM()

response = llm.generate(
    "Explain artificial intelligence in 3 simple sentences."
)

print("\n========== GEMINI LLM TEST ==========")
print(response)