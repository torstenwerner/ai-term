import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import prompt, PromptType

load_dotenv()


def generate(prompt_type: PromptType, term: str) -> str:
    """
    Generates a text response based on the given prompt type and term using the GenAI
    API client.

    :param prompt_type: Indicates the type of prompt. Must be an instance of PromptType.
    :param term: The specific term or input string used within the generated prompt.
    :return: The AI answer text as a stripped string.
    """
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt(prompt_type, term)),
            ]
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1.0
    )

    response = client.models.generate_content(
        model=os.environ.get("GOOGLE_MODEL"),
        contents=contents,
        config=generate_content_config,
    )
    return response.text.strip()


if __name__ == "__main__":
    # answer = generate(PromptType.DICTIONARY_EN, "flash")
    answer = generate(PromptType.ENCYCLOPEDIA_EN, "Python")
    Path("answer.md").write_text(answer)
