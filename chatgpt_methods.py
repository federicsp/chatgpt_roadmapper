from chatgpt_wrapper import OpenAIAPI
from db.mongo_queries import insert_word
import ast
import openai

bot = OpenAIAPI()

def ask_for_list(word1, word2, lang):
    # word2 not used atm

    if lang == "en":
        prompt = f"create a json like  dictionary of 7 key words that i should learn about {word1}, with values that are strings containing descriptions and examples. Then add a last element '{word1}': <description of  {word1}> to the dictionary. Don't give explanation and don't give a name to the dictionary. Don't use double quotes in the values"
    elif lang == "it":
        prompt = f"Creare un dizionario in italiano in formato JSON con 7 parole chiave che dovrei imparare su {word1}, con le loro dettagliate descrizioni ed esempi come valori. Aggiungere quindi un ultimo elemento '{word1}': <descrizione di {word1}> al dizionario. Non dare spiegazioni e non dare un nome al dizionario. Non usare double quotes nei valori. In italiano"
    element = ""
    for chunk in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            stream=True,
    ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            element += content
            if '",' in content or "}" in content:
                result_cg = element[:-1][: len(element)-2] + '}'
                dict_result_cg = ast.literal_eval(
                    str(result_cg).replace(".", "").replace("}{", ",").replace("]", "}").replace("}[", ",").replace(".", "").replace("} {", ",").replace(";", ",").replace("{'", '{"').replace("""": '""", '": "').replace('''': "''', '": "').replace("""", '""", '", "').replace('''': "''', '", "').replace("'}", '"}').replace("': '", '": "').replace("', '", '", "')
                ) #doesn't work very well
                list_of_8_words = [x for x in dict_result_cg.keys()]
                list_of_8_descriptions = [x for x in dict_result_cg.values()]

                words = list_of_8_words
                descriptions = list_of_8_descriptions
                prev_text = list_of_8_words[-1].split(" ")[0] + " "
                yield words, descriptions, prev_text
                if len(words) == 8:
                    insert_word(word1, dict_result_cg, lang=lang)
