import base64
import json
import zlib


def decode_blueprint_string(blueprint_string: str) -> str:
    # A blueprint string is a JSON representation of the blueprint,
    # compressed with zlib deflate using compression level 9 and
    # then encoded using base64 with a version byte in front of the
    # encoded string.

    encoded_bytes = bytearray(blueprint_string, "utf-8")
    decoded_bytes = base64.decodebytes(encoded_bytes[1:])
    decoded_string = zlib.decompress(decoded_bytes).decode("utf-8")

    return json.loads(decoded_string)
