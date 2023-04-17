from fastapi import FastAPI, Request, Response
from chatgpt_methods import ask_for_list
import json
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from db.mongo_queries import get_word, get_words_user
from static_routes import router as static_router
from settings import settings

app = FastAPI(title=settings.app_name)
app.include_router(static_router)
templates = Jinja2Templates(directory=settings.templates_directory)

@app.get("/{lang}", response_class=HTMLResponse)
async def input_words(request: Request, lang: str):
    template_name = "main.html" if lang == "en" else "main_it.html"
    items = get_words_user(lang)
    hide = "true" if items else "none"
    #implement read cookies
    return templates.TemplateResponse(template_name, {"request": request,
                                                      "hide": hide,
                                                      "items": items or [],
                                                      #"cookie_words": cookie_words
                                                      })



@app.post("/{lang}/words", response_class=HTMLResponse)
async def show_words(request: Request, lang="en"):
    form_data = await request.form()
    word1 = form_data.get('word1', 'python')
    word2 = form_data.get('word2', 'nothing')
    dict_result_cg = get_word(word1, lang)
    if dict_result_cg:
        list_of_8_words = [x for x in dict_result_cg.keys()]
        list_of_8_descriptions = [x for x in dict_result_cg.values()]
        template_file = "words_it.html" if lang == "it" else "words.html"
        response = templates.TemplateResponse(template_file,
                                              {"request": request,
                                               "words": list_of_8_words,
                                               "from_mongo": True,
                                               "descriptions": list_of_8_descriptions,
                                               "word1_description": list_of_8_descriptions[-1] if len(list_of_8_words) > 7 else "",
                                               "len_words": len(list_of_8_words),
                                               "word1": word1,
                                               "prev_text": list_of_8_words[-1].split(" ")[0]+" ",
                                               "zippone": zip(list_of_8_words,
                                                              list_of_8_descriptions,
                                                              [40, 20, 40, 54, 65, 77, 72],
                                                              [10, 20, 33, 47, 61, 74, 88])
        })
    else:
        async def stream_response():
            for context in ask_for_list(word1, word2, lang):
                words, descriptions, prev_text = context[0], context[1], context[2]
                template_file = "words_it.html" if lang == "it" else "words.html"
                template_context = {"request": request,
                                    "words": words,
                                    "descriptions": descriptions,
                                    "from_mongo": False,
                                    "len_words": len(words),
                                    "prev_text": prev_text,
                                    "word1_description": descriptions[-1] if len(words) > 7 else "",
                                    "word1": word1,
                                    "zippone": zip(words,
                                                   descriptions,
                                                   [40, 20, 40, 54, 65, 77, 72],
                                                   [10, 20, 33, 47, 61, 74, 88])
                                    }
                body = templates.TemplateResponse(template_file, template_context).body
                yield body

        response = StreamingResponse(content=stream_response())
    #implement set cookies
    return response

