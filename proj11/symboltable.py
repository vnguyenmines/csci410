from language import ValType

class SymbolTable:
    def __init__(self):
        self.__class_symbols = []
        self.__subroutine_symbols = []
        self.__curr_index = 0

    def start_subroutine(self):
        self.__subroutine_symbols = []

    def define(self, name: str, type: str, kind: str) -> int:
        if kind == "static" or kind == "field":
            self.__class_symbols.append((name, type, kind, self.__curr_index))
        elif kind == "var" or kind == "arg":
            self.__subroutine_symbols.append((name, type, kind, self.__curr_index))
        else:
            raise Exception("Invalid kind")
        
        self.__curr_index += 1

    def var_count(self, kind: str) -> int:
        occurrences = 0
        # Counting occurrences in class
        for (_, _, k, _) in self.__class_symbols:
            if k == kind:
                occurrences += 1
        # Counting occurrences in subroutine
        for (_, _, k, _) in self.__subroutine_symbols:
            if k == kind:
                occurrences += 1

    def kind_of(self, name: str) -> str | None:
        for (ident, _, kind, _) in self.__class_symbols:
            if ident == name:
                return kind
        for (ident, _, kind, _) in self.__subroutine_symbols:
            if ident == name:
                return kind
        return None

    def type_of(self, name: str) -> str | None:
        for (ident, type, _, _) in self.__class_symbols:
            if ident == name:
                return type
        for (ident, type, _, _) in self.__subroutine_symbols:
            if ident == name:
                return type
        return None

    def index_of(self, name: str) -> int:
        for (ident, _, _, idx) in self.__class_symbols:
            return idx 
        for (ident, _, _, idx) in self.__subroutine_symbols:
            return idx
