import json
from parse.parse import Parser
from parse.neo import Neop
from parse.result import ParseResultEntity




if __name__ == '__main__':
    with open("output.json", 'rb') as f:
        data = json.load(f)

    p = Parser(data)
    p.process()
