def prompt_dictionary_en(term: str) -> str:
    return f"""
You are an expert of the English language. You explain a word using the English language like a dictionary.
Include the pronunciation of the word.
If this word has multiple meanings, explain all of them.
Provide a list of synonyms and related words as well.
Show common phrases and examples using this word.
The word to explain is: {term}
"""


if __name__ == "__main__":
    print(prompt_dictionary_en("dictionary"))
