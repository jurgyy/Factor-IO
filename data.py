import glob
from os import path
import json
import pyrebase
import requests
from pyrebase.pyrebase import Database

from blueprintString import decode_blueprint_string
from config import Config


def connect_database() -> Database:
    config = {
        "authDomain": "facorio-blueprints.firebaseapp.com",
        "databaseURL": "https://facorio-blueprints.firebaseio.com",
        "apiKey": "AIzaSyAcZJ7hGfxYKhkGHJwAnsLS3z5Tg9kWw2s",
        "storageBucket": "facorio-blueprints.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    return db


def download_blueprint_summaries():
    db = connect_database()

    summaries_response = db.child("blueprintSummaries").get()
    summaries = {}

    for s in summaries_response.each():
        summaries[s.key()] = s.val()

    with open(Config.RawSummariesFName, "w") as f:
        json.dump(summaries, f)


def download_blueprints():
    db = connect_database()

    blueprint_response = db.child("blueprints").get()
    bps = {}
    for b in blueprint_response.each():
        bps[b.key()] = b.val()

    with open(Config.RawBlueprintDataFName, "w") as f:
        json.dump(bps, f)


def load_raw_blueprints() -> dict:
    with open(Config.RawBlueprintDataFName) as f:
        return json.load(f)


def get_factorio_prints_tags() -> dict:
    r = requests.get(Config.TagsUrl)
    return json.loads(r.text)


def filter_mod_tags(raw_factorioprints_data: dict) -> dict:
    tags: dict = get_factorio_prints_tags()

    tag_key = Config.FactorioPrintsTagKey
    base_mod_tag = Config.FactorioPrintsModTag
    mod_tag_strings = [f"/{base_mod_tag}/{t}/" for t in tags[base_mod_tag] if t != "vanilla"]

    filtered_blueprints = {}
    for fp_key, raw_fp_data in raw_factorioprints_data.items():
        if tag_key in raw_fp_data and any(tag in raw_fp_data[tag_key] for tag in mod_tag_strings):
            continue
        filtered_blueprints[fp_key] = raw_fp_data

    return filtered_blueprints


def store_blueprints(factorioprints_data: dict, max_blueprint_size=1000000):
    for k, v in factorioprints_data.items():
        if len(v["blueprintString"]) > max_blueprint_size:
            continue
        try:
            blueprint = decode_blueprint_string(v["blueprintString"])
            with open(f"{path.join(Config.BlueprintsDir, k)}.json", "w") as f:
                json.dump(blueprint, f)
        except:
            print(f"Failed to store blueprint for key {k}.")


def iter_stored_blueprints():
    for bp_path in glob.glob(path.join(Config.BlueprintsDir, "*.json")):
        base = path.basename(bp_path)
        key = path.splitext(base)[0]

        with open(bp_path) as f:
            yield key, json.load(f)


if __name__ == "__main__":
    # download_blueprints()

    raw = load_raw_blueprints()
    filtered = filter_mod_tags(raw)
    store_blueprints(filtered)

    for k, d in iter_stored_blueprints():
        print(k, d)
        break
