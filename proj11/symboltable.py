from language import ValType

class SymbolTable:
    def __init__(self):
        self.__class_symbols = []
        self.__subroutine_symbols = []
        self.__index = {
            "arg": 0,
            "static": 0,
            "var": 0,
            "field": 0
        }

    def start_subroutine(self):
        self.__subroutine_symbols = []
        self.__index["static"] = 0
        self.__index["field"] = 0
        self.__index["var"] = 0
        self.__index["arg"] = 0

    def define(self, name: str, type: str, kind: str) -> int:
        match kind:
            case "static":
                self.__class_symbols.append((name, type, kind, self.__index["static"]))
                self.__index["static"] += 1
            case "field":
                self.__class_symbols.append((name, type, kind, self.__index["field"]))
                self.__index["field"] += 1
            case "var":
                self.__subroutine_symbols.append((name, type, kind, self.__index["var"]))
                self.__index["var"] += 1
            case "arg":
                self.__subroutine_symbols.append((name, type, kind, self.__index["arg"]))
                self.__index["arg"] += 1
            case _:
                raise Exception("Invalid kind")

    def var_count(self, kind: str) -> int:
        occurrences = 0
        # Counting occurrences in subroutine
        for (_, _, k, _) in self.__subroutine_symbols:
            if k == kind:
                occurrences += 1
        # Counting occurrences in class
        for (_, _, k, _) in self.__class_symbols:
            if k == kind:
                occurrences += 1
        
        return occurrences

    def kind_of(self, name: str) -> str | None:
        for (ident, _, kind, _) in self.__subroutine_symbols:
            if ident == name:
                return kind
        for (ident, _, kind, _) in self.__class_symbols:
            if ident == name:
                return kind
        return None

    def type_of(self, name: str) -> str | None:
        for (ident, type, _, _) in self.__subroutine_symbols:
            if ident == name:
                return type
        for (ident, type, _, _) in self.__class_symbols:
            if ident == name:
                return type
        return None

    def index_of(self, name: str) -> int:
        for (ident, _, _, idx) in self.__subroutine_symbols:
            if ident == name:
                return idx
        for (ident, _, _, idx) in self.__class_symbols:
            if ident == name:
                return idx 
        # return self.__curr_index
        return None