import json

def load_json(path):
    try:
        with open(path) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
            return jsonObject
    except:
        return dict()