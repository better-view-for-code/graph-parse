import json

from parse.parse import Parser

if __name__ == '__main__':
    with open("output.json", 'rb') as f:
        data = json.load(f)

    p = Parser(data)
    p.process()
