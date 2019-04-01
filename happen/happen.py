import ast
import random
import sys


class KeywordListener(ast.NodeTransformer):
    def __init__(self, keywords, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = keywords

    def visit_Delete(self, node):
        if any(filter(lambda target: target.id in self.keywords, node.targets)):
            raise SyntaxError("can't delete keyword")

        return node

    def visit_Assign(self, node):
        if any(filter(lambda target: target.id in self.keywords, node.targets)):
            raise SyntaxError("can't assign to keyword")

        return node


def keyword_patcher(keywords, name, *args, **kwargs):
    module = __import__(name, *args, **kwargs)
    if module.__name__ != "__main__" and not hasattr(module, "__file__"):
        return module

    tree = ast.parse(
        "".join(open(sys.modules[name].__file__.replace("pyc", "py"), "r").readlines())
    )
    tree = KeywordListener(keywords).visit(tree)
    ast.fix_missing_locations(tree)
    return compile(tree, name, "exec")
