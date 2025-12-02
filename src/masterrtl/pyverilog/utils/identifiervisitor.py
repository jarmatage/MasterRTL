# -------------------------------------------------------------------------------
# identifiervisitor.py
#
# Identifier list generator in a nested operator
#
# Copyright (C) 2015, Shinya Takamaeda-Yamazaki
# License: Apache 2.0
# -------------------------------------------------------------------------------

from masterrtl.pyverilog.dataflow.visit import NodeVisitor


def getIdentifiers(node):
    v = IdentifierVisitor()
    v.visit(node)
    ids = v.getIdentifiers()
    return ids


class IdentifierVisitor(NodeVisitor):
    def __init__(self):
        self.identifiers = []

    def getIdentifiers(self):
        return tuple(self.identifiers)

    def reset(self):
        self.identifiers = []

    def visit_Identifier(self, node):
        self.identifiers.append(node.name)
