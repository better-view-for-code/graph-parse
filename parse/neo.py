from py2neo import Graph, Node, Relationship

from config import Config
from parse.result import ParseResultEntity, ParseResultRel
from py2neo import NodeMatcher, RelationshipMatcher


class Neop(object):
    def __init__(self):
        self.g = Graph(host=Config['host'],
                       port=Config['port'],
                       user=Config['user'],
                       password=Config['password'])

    def select_entity(self, ent: ParseResultEntity):
        matcher = NodeMatcher(self.g)
        node = matcher.match(ent.type, name=ent.name).first()
        return node

    def entity_exists(self, ent: ParseResultEntity):
        node = self.select_entity(ent)
        return node is not None

    def create_entity(self, ent: ParseResultEntity):
        self._add_entity(ent.type, **ent.properties)

    def update_entity(self, ent: ParseResultEntity):
        matcher = NodeMatcher(self.g)
        node = matcher.match(ent.type, name=ent.name).first()
        if node:
            node.update(**ent.properties)
            self.g.push(node)
        else:
            self.create_entity(ent)

    def select_rel(self, rel: ParseResultRel):
        matcher = RelationshipMatcher(self.g)
        source = self.select_entity(rel.source)
        target = self.select_entity(rel.target)
        rel = matcher.match([source, target], rel.rel).first()
        return rel

    def exists_rel(self, rel: ParseResultRel):
        rel = self.select_rel(rel)
        return rel is not None

    def create_rel(self, rel: ParseResultRel):
        source = self.select_entity(rel.source)
        target = self.select_entity(rel.target)
        self._add_relation(source, target, rel.rel, **rel.properties)

    def update_rel(self, rel: ParseResultRel):
        reln = self.select_rel(rel)
        if reln:
            reln.update(**rel.properties)
            self.g.push(reln)
        else:
            self.create_rel(rel)

    def _add_entity(self, kind, **properties):
        node = Node(kind, **properties)
        self.g.create(node)
        return node

    def _list_entity(self):
        n = self.g.run("MATCH (n) RETURN distinct labels(n) as l")
        return [t['l'][0] for t in n.data()]

    def _delete_entity(self, kind):
        # delete relation first
        rs = self.get_relation_by_entity(kind)
        for r in rs:
            self.delete_relation(r)

        n = self.g.run(f"MATCH (n: {kind}) delete n")
        return n.data()

    def _add_relation(self, n1, n2, r, **properties):
        r = Relationship(n1, r, n2, **properties)
        self.g.create(r)
        return r

    def _list_relation(self):
        n = self.g.run("MATCH (s) - [r] -> (t) RETURN distinct type(r) as l")
        return [l['l'] for l in n.data()]

    def _delete_relation(self, rel):
        r = self.g.run(f"match (s) - [r: {rel}] -> (t) delete r")
        return r

    def _get_relation_by_entity(self, ent):
        n = self.g.run(f"MATCH (s:{ent}) - [r] -> (t) RETURN distinct type(r) as l")
        n1 = self.g.run(f"MATCH (s) - [r] -> (t:{ent}) RETURN distinct type(r) as l")
        return [l['l'] for l in n.data()] + [l['l'] for l in n1.data()]
