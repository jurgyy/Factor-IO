from os import path


class Config:
    DataDir: str = path.join(path.dirname(__file__), "data")
    RawDir: str = path.join(DataDir, "raw")
    RawBlueprintDataFName: str = path.join(RawDir, "rawdata.json")
    RawSummariesFName: str = path.join(RawDir, "rawsummaries.json")
    BlueprintsDir: str = path.join(DataDir, "blueprints")

    TagsUrl: str = "https://raw.githubusercontent.com/FactorioBlueprints/factorio-prints/master/data/tags.json"
    FactorioPrintsModTag: str = "mods"
    FactorioPrintsTagKey = "tags"

    EntitySizeJsonFName: str = path.join(DataDir, "size.json")
