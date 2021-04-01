from Blueprint.BlueprintWrapper import BlueprintWrapper
from data import iter_stored_blueprints

iterator = iter_stored_blueprints()

for i, (k, bp) in enumerate(iterator):
    if i > 50:
        break

    wrapper = BlueprintWrapper(**bp)
    print(k, wrapper)

