import base64
import json
import zlib


def decode_blueprint_string(blueprint_string: str) -> dict:
    # A blueprint string is a JSON representation of the blueprint,
    # compressed with zlib deflate using compression level 9 and
    # then encoded using base64 with a version byte in front of the
    # encoded string.

    encoded_bytes = bytearray(blueprint_string, "utf-8")
    decoded_bytes = base64.decodebytes(encoded_bytes[1:])
    decoded_string = zlib.decompress(decoded_bytes).decode("utf-8")

    return json.loads(decoded_string)


def encode_blueprint_dict(blueprint_dict: dict) -> str:
    js = json.dumps(blueprint_dict)
    encoded_bytes = zlib.compress(bytearray(js, encoding="utf-8"), 9)
    encoded_string: str = base64.b64encode(encoded_bytes).decode("utf-8", "ignore")
    return "0" + str(encoded_string)


def _main():
    s = "0eNp9kO1qwzAMRd/l/rZLvrqmfpUyhpNqnSBWgq2OheB3X9LA2NjYzyuODrpa0A13miKLwi3gfpQEd1mQ+CZ+2GY6TwQHVgowEB+25FOi0A" \
        "0sNxt8/8ZCtkY2YLnSB1yZnw1IlJVp9z3C/CL30FFcgf9NBtOY1uVRtgtWoT23h6PBDNe0xeGYs/mlrL6Urz6p1eglTWNU29GgfxjLovihN" \
        "LhypH5Hqq3Ao7L79iGDd4ppB9qyOZ2rU/3UNEVd5fwJp9xrmA=="

    d = decode_blueprint_string(s)
    r = encode_blueprint_dict(d)
    rd = decode_blueprint_string(r)

    print(s)
    print(r)
    print(d)
    print(rd)

    assert(rd == d)


if __name__ == '__main__':
    _main()
