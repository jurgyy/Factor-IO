from Blueprint.BlueprintWrapper import BlueprintWrapper
from blueprintString import decode_blueprint_string


def test():
    d = decode_blueprint_string("0eNqlkdGqwjAQRP9lnlMxaayaXxG5tNdVAu22JFu5peTfb1tfBEURH2fZOTvsjKjqnrrgWeBG+N+WI9xhRPQXLut5JkNHcPBCDRS4bGZ1LqNkEkqOXRskq6gWJAXPJ/qD0+moQCxePN1wixh+uG8qCtPCS5BC18bJ2/J8f+Jl2ujVRmGAs4VdbVJSD0jzKVLv3yHzL1IWz5H2i5QLcnrs0oS7K07hSiEuLrPTdrs327ywdp2blP4BuTudFg==")
    w = BlueprintWrapper(**d)
    for bp in w:
        print(bp)


if __name__ == "__main__":
    test()
