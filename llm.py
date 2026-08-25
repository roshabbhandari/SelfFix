import os

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "gemini").lower()


def call_llm(system_prompt: str, user_prompt: str) -> str:
    if LLM_PROVIDER == "gemini":
        from google import genai
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set.")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\n\n{user_prompt}",
        )
        return response.text

    if LLM_PROVIDER == "groq":
        from groq import Groq
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set.")
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content

    raise ValueError(
        f"Unknown LLM_PROVIDER '{LLM_PROVIDER}'. Use 'gemini' or 'groq'."
    )
