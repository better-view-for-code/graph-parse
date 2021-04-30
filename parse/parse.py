import json
from utils.dim_dict import symbol_dict
from utils.base_type import SCALA_BASE_TYPE
from .result import ParseResultEntity, ParseResultRel
from .neo import Neop


class Parser(object):

    def __init__(self, lines):
        self.lines = lines
        self.neo = Neop()

    def process(self):
        for line in self.lines:
            self.parse_line(line)

    def parse_line(self, obj):
        source_base_type = False
        target_base_type = False

        print(f"deal {obj}")

        sym = obj['sym']
        sym_target = obj['uses']

        for ss in sym:
            if ss in SCALA_BASE_TYPE:
                source_base_type = True

        for ss in sym_target:
            if ss in SCALA_BASE_TYPE:
                target_base_type = True

        if source_base_type and not target_base_type:
            self.parse_sym(sym_target)

        if not source_base_type and target_base_type:
            self.parse_sym(sym)

        if not source_base_type and not target_base_type:
            source = self.parse_sym(sym)
            target = self.parse_sym(sym_target)
            rel = ParseResultRel("uses", source, target)
            self.neo.update_rel(rel)

    def parse_sym(self, syms):

        res = []
        for sym in syms:
            dim, name = symbol_dict[sym.split(":")[0]], sym.split(":")[1]
            ent = ParseResultEntity(dim, name)
            self.neo.update_entity(ent)
            res.append(ent)

        if len(res) < 2:
            return res[0]

        for i in range(len(res) - 2):
            source = res[i]
            target = res[i + 1]
            rel = ParseResultRel("contains", source, target)
            self.neo.update_rel(rel)

        return res[-1]
