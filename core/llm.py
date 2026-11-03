import os
from google import genai


class LLM:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"

    def generate(self, prompt):

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            if response and response.text:
                return response.text

            return "Gemini returned an empty response."

        except Exception as error:

            print("\n⚠ Gemini request failed.")
            print(f"Reason: {type(error).__name__}")
            print("DHMIF will continue using its fallback mechanism.")

            return (
                "Fallback response: "
                "Gemini was temporarily unavailable, "
                "so the DHMIF workflow continued."
            )