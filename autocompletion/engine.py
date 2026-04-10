

import importlib
from parser import analyze_code

class AutoCompleteEngine:

    def __init__(self, source_code):
        self.source_code = source_code
        self.symbols, self.imports = analyze_code(source_code)

    def suggest(self, text_before_cursor):
        if "." in text_before_cursor:
            return self._attribute_suggestions(text_before_cursor)

        return self._global_suggestions(text_before_cursor)

    def _global_suggestions(self, prefix):
        return [name for name in self.symbols.keys()
                if name.startswith(prefix)]

    def _attribute_suggestions(self, text):
        object_name = text.split(".")[-2]

        if object_name in self.imports:
            module = importlib.import_module(self.imports[object_name])
            return [attr for attr in dir(module)
                    if not attr.startswith("_")]

        return []