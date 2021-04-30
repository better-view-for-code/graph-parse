import json


class ParseResultEntity:
    def __init__(self, tpe, name):
        self.type = tpe
        self.name = name
        self.properties = {"name": self.name}


    def __str__(self):
        return f"ent: {self.type}, properties: {json.dumps(self.properties)}"


class ParseResultRel:
    def __init__(self, rel, source, target):
        self.rel = rel
        self.source = source
        self.target = target
        self.properties = {}

    def set_source(self, source):
        self.source = source

    def set_target(self, target):
        self.target = target

    def __str__(self):
        return f"rel: {self.rel}"
