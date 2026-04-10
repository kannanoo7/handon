import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.symbols = {}
        self.imports = {}

    def visit_Import(self, node):
        for alias in node.names:
            module_name = alias.name
            as_name = alias.asname if alias.asname else module_name
            self.imports[as_name] = module_name

    def visit_FunctionDef(self, node):
        self.symbols[node.name] = "function"
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.symbols[node.name] = "class"
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.symbols[target.id] = "variable"
        self.generic_visit(node)


def analyze_code(source_code):
    tree = ast.parse(source_code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.symbols, analyzer.imports