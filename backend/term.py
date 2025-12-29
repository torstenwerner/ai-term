import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import prompt_dictionary_en

load_dotenv()


def generate(term: str) -> str:
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    # model = "gemini-2.0-flash-lite"
    model = "gemini-2.5-flash-lite"
    # model = "gemini-2.5-flash"
    # model = "gemini-3-flash-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt_dictionary_en(term)),
            ]
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1.0
    )

    response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
    )
    print(response.text.strip())
    return "failed to generate answer"


if __name__ == "__main__":
    answer = generate("dictionary")
    print(answer)
