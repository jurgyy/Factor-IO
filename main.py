import TestPackage

data: dict = \
    {
        "b":
            {
                "c":
                    {
                        "bp":
                            {
                                "p": 0
                            },
                    },
            },
    }

TestPackage.Wrapper(**data)
print(1)


# from Blueprint.BlueprintWrapper import BlueprintWrapper
# from data import iter_stored_blueprints
#
# iterator = iter_stored_blueprints()
#
# for k, bp in iterator:
#     print(k, bp)
#     wrapper = BlueprintWrapper(**bp)
#     print(wrapper)
#     break
