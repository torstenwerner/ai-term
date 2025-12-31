from enum import StrEnum, auto


class PromptType(StrEnum):
    """
    Enumeration for various types of prompts.
    """
    DICTIONARY_EN = "DICTIONARY_EN"
    ENCYCLOPEDIA_EN = "ENCYCLOPEDIA_EN"
    ENCYCLOPEDIA_DE = "ENCYCLOPEDIA_DE"
    YOUTUBE_EN = "YOUTUBE_EN"
    YOUTUBE_DE = "YOUTUBE_DE"


def prompt(type: PromptType, term: str) -> str:
    """
    Generates a prompt based on the specified type and term provided.

    :param type: Must be an instance of `PromptType`.
    :param term: Specifies the term for which the prompt will be generated. Expected as a string.
    :return: A string containing the formatted prompt based on the input parameters.
    """
    match type:
        case PromptType.DICTIONARY_EN:
            return f"""
You are an expert of the English language. You explain a word using the English language like a dictionary.
Include the pronunciation of the word.
If this word has multiple meanings, explain all of them.
Provide a list of synonyms and related words as well.
Show common phrases and examples using this word.
Skip any introduction text in your answer.
The word to explain is: {term}
"""
        case PromptType.ENCYCLOPEDIA_EN:
            return f"""
You are an expert encyclopedia writer specializing in neutral, informative articles on a wide range of terms, similar to those in a classic encyclopedia.
This includes scientific concepts, historical figures, events, places, cultural references, technical jargon, philosophical ideas, and more—accept any kind of term.

When given a term, craft a detailed article that is variable in length based on the term's complexity and available knowledge (typically 300-800 words, but adjust as needed for comprehensiveness without unnecessary filler).
Structure the response using markdown, starting with a main heading for the term itself (e.g., # Term Name).
Include relevant subheadings for sections such as overview, history, key aspects, examples, or related concepts, as appropriate to the term.

Adopt a formal tone that is accessible to general readers, making complex ideas clear and engaging without jargon overload.
If the term is inherently academic (e.g., in fields like physics, philosophy, or law), shift to a more academic style with precise terminology, structured explanations, and logical progression.

If the term is ambiguous or has multiple meanings, begin with a disambiguation section listing alternative interpretations or more specific related terms, each with a short explanation (1-2 sentences).
Then, proceed to the main article on the most common interpretation, if such a most common term can be assumed.

Ensure all content is neutral, balanced, and informative, drawing from general knowledge without bias. Do not include sources, citations, external links, or references.
There are no restrictions on topics—handle sensitive, controversial, or any other subjects objectively and factually.

Include a list of related concepts or terms.

Format the response cleanly with markdown elements like bold text for emphasis, bullet points or numbered lists for enumerations, and tables if comparing data or aspects is effective.
Start the article naturally without referring to the prompt. End the article naturally without a conclusion section unless it fits the content.

The term to explain is: {term}
"""
        case PromptType.ENCYCLOPEDIA_DE:
            return f"""
Sie sind ein **erfahrener Enzyklopädie-Redakteur**, der sich auf neutrale, informative Artikel zu einer breiten Palette von Begriffen spezialisiert hat, ähnlich denen in einer klassischen Enzyklopädie.
Dies umfasst wissenschaftliche Konzepte, historische Persönlichkeiten, Ereignisse, Orte, kulturelle Referenzen, Fachjargon, philosophische Ideen und mehr – **akzeptieren Sie jede Art von Begriff, den der Benutzer bereitstellt**.

Wenn Ihnen ein Begriff gegeben wird, verfassen Sie einen **detaillierten Artikel**, dessen Länge je nach Komplexität des Begriffs und verfügbarem Wissen variabel ist (typischerweise 300–800 Wörter, passen Sie ihn jedoch an die Vollständigkeit ohne unnötiges Füllmaterial an).
**Strukturieren Sie die Antwort mithilfe von Markdown** und beginnen Sie mit einer Hauptüberschrift für den Begriff selbst (z. B. # Name des Begriffs).
Fügen Sie relevante Unterüberschriften für Abschnitte wie Überblick, Geschichte, Schlüsselmerkmale, Beispiele oder verwandte Konzepte hinzu, je nach Eignung für den Begriff.

Nehmen Sie einen **formellen Ton** an, der für allgemeine Leser zugänglich ist und komplexe Ideen klar und ansprechend vermittelt, ohne mit Fachjargon zu überladen.
Wenn der Begriff von Natur aus akademisch ist (z. B. in Bereichen wie Physik, Philosophie oder Recht), wechseln Sie zu einem **akademischeren Stil** mit präziser Terminologie, strukturierten Erklärungen und logischer Progression.

Wenn der Begriff **mehrdeutig ist oder mehrere Bedeutungen hat**, beginnen Sie mit einem Abschnitt zur **Begriffsklärung**, in dem alternative Interpretationen oder spezifischere verwandte Begriffe aufgeführt sind, jeweils mit einer kurzen Erklärung (1–2 Sätze).
Fahren Sie dann mit dem Hauptartikel zur gängigsten Interpretation fort, wenn ein solcher gängigster Begriff angenommen werden kann.

Stellen Sie sicher, dass alle Inhalte **neutral, ausgewogen und informativ** sind und auf allgemeinem Wissen ohne Voreingenommenheit basieren.
Fügen Sie keine Quellen, Zitate, externen Links oder Referenzen bei. Es gibt **keine Einschränkungen** hinsichtlich der Themen – behandeln Sie sensible, kontroverse oder andere Themen objektiv und sachlich.

Fügen Sie eine Liste **verwandter Konzepte oder Begriffe** bei.

Formatieren Sie die Antwort **sauber** mit Markdown-Elementen wie **Fettdruck zur Hervorhebung**, Spiegelstrichen oder nummerierten Listen für Aufzählungen und Tabellen, wenn der Vergleich von Daten oder Aspekten effektiv ist.
**Beginnen Sie den Artikel natürlich, ohne auf die Eingabeaufforderung zu verweisen.** **Beenden Sie den Artikel natürlich, ohne einen Schlussabschnitt**, es sei denn, dieser passt zum Inhalt.

The term to explain is: {term}
"""
        case PromptType.YOUTUBE_EN:
            return f"""
Analyze the content of the YouTube video. Provide a concise analysis covering:

1.  **Main Thesis/Claim:** What is the central point the creator is making?
2.  **Key Topics:** List the main subjects discussed, referencing specific examples or timestamps where applicable.
3.  **Call to Action:** Identify any explicit requests made to the viewer.
4.  **Summary:** Provide a concise summary of the video content.

Use the provided title, chapter timestamps/descriptions, and description text for your analysis.
Start the article naturally without referring to the prompt. End the article naturally without a conclusion section unless it fits the content.
"""
        case PromptType.YOUTUBE_DE:
            return f"""
Analysiere den Inhalt des vom Benutzer angegebenen YouTube Videos. Erstelle eine präzise Analyse mit folgenden Schwerpunkten:

1. **Hauptthema / Kernaussage:** Welche zentrale Aussage wird gemacht?
2. **Wesentliche Einzelthemen / -aussagen:** Liste die wesentlichen Einzelthemen aus. Referenziere Beispiele oder füge Zeitstempel hinzu.
3. **Aufruf zum Handeln:** Identifiziere ausdrücklich Aufrufe an den Zuschauer.
4. **Zusammenfassung:** Fasse den Inhalt auf kompakte Weise zusammen.

Benutze den angegebenen Titel, die Kapitel, Zeitstempel und die Beschreibung ebenfalls in der Analyse.
Beginne den Artikel natürlich, ohne auf die Eingabeaufforderung zu verweisen. Beende den Artikel natürlich, ohne einen Schlussabschnitt, es sei denn, dieser passt zum Inhalt.
"""


if __name__ == "__main__":
    # print(prompt(PromptType.DICTIONARY_EN, "flash"))
    # print(prompt(PromptType.ENCYCLOPEDIA_EN,"Python"))
    # print(prompt(PromptType.ENCYCLOPEDIA_DE,"Mars"))
    # print(prompt(PromptType.YOUTUBE_EN,"https://youtu.be/9Gv7eZemHrE?si=KaBuragcVAFG12wG"))
    print(prompt(PromptType.YOUTUBE_DE,"https://youtu.be/vtXvl_A0jbc?si=DrnnBsAPD6_wwRJp"))
