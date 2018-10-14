from google.protobuf.json_format import MessageToJson
from flask import Flask, render_template, request
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import language
import json
import os


app = Flask(__name__)


def get_story_text(storyname, position):
    ret = None
    with open('stories' + os.sep + storyname + '.txt', 'r') as fp:
        for i, line in enumerate(fp):
            if i == position:
                ret = line.strip()
    return ret


def get_story_count(storyname):
    cnt = 0
    with open('stories' + os.sep + storyname + '.txt', 'r') as fp:
        for i, line in enumerate(fp):
            if i != 0:
                cnt += 1
    return cnt


@app.route("/text", methods=['GET'])
def text():
    if int(request.args.get('position')) == 0:
        return json.dumps({"chapter": get_story_text(request.args.get('story'), int(request.args.get('position'))), "length": get_story_count(request.args.get('story'))})
    client = language.LanguageServiceClient()
    para = get_story_text(request.args.get('story'), int(request.args.get('position')))
    d = {"lines": []}

    document = types.Document(content=para, type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(document=document, encoding_type='UTF32')
    response = json.loads(MessageToJson(response, preserving_proto_field_name=True))

    texts = []
    contents = [x["text"]["content"] for x in response["sentences"]]
    for i, sent in enumerate(response["sentences"]):
        t = {"start": None, "end": len(para) - 1, "content": contents[i]}
        if "begin_offset" in sent["text"]:
            t["start"] = int(sent["text"]["begin_offset"])
            texts[i - 1]["end"] = t["start"]
        else:
            t["start"] = 0
        texts.append(t)

    for i, text in enumerate(texts):
        l = {"line": i, "entities": []}
        t = []
        check = False
        for token in response["tokens"]:
            offset = None
            if "begin_offset" not in token["text"]:
                offset = 0
            else:
                offset = int(token["text"]["begin_offset"])
            if offset < text["start"]:
                continue
            if offset >= text["end"]:
                break
            if token["part_of_speech"]["tag"] == 'NOUN':
                if "proper" in token["part_of_speech"]:
                    if not check and len(t) != 0:
                        if any(x[0].isupper() for x in t) or len(t) > 1:
                            l["entities"].append(' '.join(list(set(t))))
                        t = []
                    t.append(token["text"]["content"])
                    check = True
                else:
                    if check and len(t) != 0:
                        l["entities"].append(' '.join(list(set(t))))
                        t = []
                    if token["part_of_speech"]["number"] == 'SINGULAR' and token["dependency_edge"]["label"] not in ["POBJ"]:
                        t.append(token["text"]["content"])
                    check = False
        if any(x[0].isupper() for x in t):
            l["entities"].append(' '.join(list(set(t))))
        l["entities"] = list(set(l["entities"]))
        if len(l["entities"]) == 1 and len([word for word in l["entities"][0].split(' ')]) == 1 and i != 0:
            l["entities"] = [d["lines"][i - 1]["entities"][0], l["entities"][0]]
        l["content"] = text["content"]
        d["lines"].append(l)
    return json.dumps(d)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
