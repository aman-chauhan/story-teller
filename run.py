# flask packages
from flask import Flask, render_template, request

# google protobuf package for json conversion
from google.protobuf.json_format import MessageToJson

# google natural language packages
from google.cloud.language import types as ltypes
from google.cloud.language import enums
from google.cloud import language

# google computer vision packages
from google.cloud.vision import types as vtypes
from google.cloud import vision

# python packages
import requests
import base64
import json
import math
import io
import os


app = Flask(__name__)
textclient = language.LanguageServiceClient()
imageclient = vision.ImageAnnotatorClient()


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
    para = get_story_text(request.args.get('story'), int(request.args.get('position')))
    d = {"lines": []}

    document = ltypes.Document(content=para, type=enums.Document.Type.PLAIN_TEXT)
    response = textclient.analyze_syntax(document=document, encoding_type='UTF32')
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
                    if not check and len(t) > 1:
                        # if any(x[0].isupper() for x in t) or len(t) > 1:
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
        # if any(x[0].isupper() for x in t):
        if not check and len(t) > 1:
            l["entities"].append(' '.join(list(set(t))))
        if check and len(t) != 0:
            l["entities"].append(' '.join(list(set(t))))
        l["entities"] = list(set(l["entities"]))
        l["content"] = text["content"]
        d["lines"].append(l)
    return json.dumps(d)


@app.route("/image", methods=['GET'])
def image():
    query = request.args.get('query')
    terms = request.args.get('terms')
    URL = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': os.environ['GOOGLE_CUSTOM_SEARCH'],
        'exactTerms': terms,
        'searchType': 'image',
        'key': os.environ['GOOGLE_API_KEY']
    }
    r = requests.get(url=URL, params=params)
    d = r.json()
    id = -1
    for i in range(len(d["items"])):
        if any([(x in d["items"][i]["snippet"]) for x in query.split(' ')]):
            id = i
            break
    URL = d["items"][i]["link"]
    mime = d["items"][i]["mime"]
    r = requests.get(URL)
    image = vtypes.Image(content=r.content)
    client = vision.ImageAnnotatorClient()
    response = imageclient.web_detection(image=image)
    response = json.loads(MessageToJson(response, preserving_proto_field_name=True))
    t = {"imagedata": '', "color": '', 'mime': mime}
    if 'web_detection' in response and 'web_entities' in response['web_detection']:
        for entity in response["web_detection"]["web_entities"]:
            if 'description' in entity and terms in entity['description'].lower():
                t["imagedata"] = base64.b64encode(r.content).decode('utf-8')
                response = imageclient.image_properties(image=image)
                response = json.loads(MessageToJson(response, preserving_proto_field_name=True))
                color = response["image_properties_annotation"]["dominant_colors"]["colors"][0]["color"]
                cred = math.floor(color["red"])
                cgreen = math.floor(color["green"])
                cblue = math.floor(color["blue"])
                t["color"] = 'rgb({},{},{})'.format(cred, cgreen, cblue)
                return json.dumps(t)
    return json.dumps(t)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False)
