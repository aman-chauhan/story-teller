# STORY TELLER

***Generating visual narrative for stories using Computer Vision and Natural Language Processing***

## Prerequisites

### Story

The story is stored inside ```stories``` folder.

For demo, we are using an excerpt from Harry Potter and The Sorcerer's Stone, stored as ```hp.txt```.

Chapter titles follow this convention - ```!-<chapter number>-<chapter name>```. Example - ```!-1-The Boy Who Lived```

Each line in the file is a paragraph.

### Google Cloud Platform
- Setup a service account key, and store the associated json safely on your machine.
- Setup a Google Custom Search Engine with CreativeWork schema as restriction, and Image Search turned on.
- Setup an API key with Google Cloud Platform to make API calls to your search engine.

### Server and REST APIs
- [Flask](http://flask.pocoo.org/)
- [Google Language API](https://googleapis.github.io/google-cloud-python/latest/language/index.html)
- [Google Vision API](https://googleapis.github.io/google-cloud-python/latest/language/index.html)
- [Google Protobuf](https://developers.google.com/protocol-buffers/)

### Environment
Set the following Environment Variables

```shell
GOOGLE_APPLICATION_CREDENTIALS = "/path/to/your/service/account/json file"
GOOGLE_CUSTOM_SEARCH = "The ID of your Custom Search Engine."
GOOGLE_API_KEY = "The API key you set up above."
```

## How to Start Server

```
    $ FLASK_APP=run.py flask run
```

The website will be hosted on http://127.0.0.1:5000.
