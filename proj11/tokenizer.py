import re
from language import keywords, Keyword, TokenType, symbols

class JackTokenizer:
    def __init__(self, file_path) -> None:
        # Read in .jack file
        with open(file_path) as f:
            self.raw_code_lines = f.readlines()
        # Clean code
        # Remove comments
        self.cleaned_code_lines = []
        multi_line_comment = False
        for code_line in self.raw_code_lines:
            # Continuing multiline comment
            # does not terminate in current line
            if multi_line_comment and "*/" not in code_line:
                continue
            # does terminate in current line
            if multi_line_comment and "*/" in code_line:
                remaining_line = code_line[code_line.index("*/") + 2:]
                if len(remaining_line.strip()) != 0: self.cleaned_code_lines.append(remaining_line) 
                multi_line_comment = False
                code_line = code_line[code_line.index("*/") + 2:]
            
            code_line = code_line.replace("\n", "")
            code_line = code_line.replace("\t", "")
            if len(code_line) == 0: continue

            # Comment at the beginning of the line
            if "//" in code_line and code_line.index("//") == 0:
                continue
            # Comment midway through the line
            elif "//" in code_line:
                prior_to_comment = code_line[:code_line.index("//")].strip()
                if len(prior_to_comment) != 0: self.cleaned_code_lines.append(prior_to_comment) 
            # Multiline comment
            elif "/*" in code_line:
                prior_to_multi_line_comment = code_line[:code_line.index("/*")]
                if len(prior_to_multi_line_comment.strip()) != 0: self.cleaned_code_lines.append(prior_to_multi_line_comment)
                multi_line_comment = True
            else:
                self.cleaned_code_lines.append(code_line.strip())
            
            # Continuing multiline comment
            # does not terminate in current line
            if multi_line_comment and "*/" not in code_line:
                continue
            # does terminate in current line
            if multi_line_comment and "*/" in code_line:
                remaining_line = code_line[code_line.index("*/") + 2:]
                if len(remaining_line.strip()) != 0: self.cleaned_code_lines.append(remaining_line) 
                multi_line_comment = False
                continue

        # Tokens
        self.tokens = []
        for line in self.cleaned_code_lines:
            if len(line) == 0: continue
            split_line = []
            # Detecting if any strings are present
            if "\"" in line and "\\\"" not in line:
                split_line = line.split("\"")
                split_line[1] = "\"" + split_line[1] + "\""
            else:
                split_line.append(line)
            # Removed whitespaces ande extract any symbols that are grouped along in the same token
            for s in split_line:
                if s[0] == "\"" and s[len(s) - 1] == "\"":
                    self.tokens.append(s) 
                    continue
                for token in s.split(" "):
                    # Handling strings
                    # Check if any symbols are present in the current token
                    symbols_present = []
                    for c in token:
                        if c in symbols:
                            symbols_present.append(c)
                    # Handling when symbols are present 
                    if len(symbols_present) != 0:
                        seperated_tokens = []
                        for s in symbols_present:
                            # first part before symbol
                            beg = token[:token.index(s)]
                            if len(beg) != 0: seperated_tokens.append(beg)
                            # symbol
                            seperated_tokens.append(s)
                            # remaining part of the symbol
                            token = token[token.index(s) + 1:]
                        if len(token) != 0: seperated_tokens.append(token)
                        self.tokens.extend(seperated_tokens)
                    else:
                        self.tokens.append(token)
            
        self.tokens = list(filter(lambda x: x.strip() != "", self.tokens))

    def has_more_tokens(self) -> bool:
        return len(self.tokens) != 0

    def advance(self) -> str:
        return self.tokens.pop(0)
    
    def curr_token(self) -> str:
        return self.tokens[0]

    def token_type(self) -> TokenType:
        curr_token = self.tokens[0].strip()

        # Keyword or symbol checking
        if curr_token in keywords:
            return TokenType.KEYWORD
        elif curr_token in symbols:
            return TokenType.SYMBOL
        # Literals
        # regex: one or more characters in the range of 0-9
        elif re.fullmatch("[0-9]+", curr_token):
            return TokenType.INT_CONST
        # regex: the first character must be an alphabetical character. Following characters can be zero or more alphabetical, numerical, or an underscore
        elif re.fullmatch("^[a-zA-Z][a-zA-Z0-9_]*", curr_token):
            return TokenType.IDENTIFIER
        # regex: surrounding quotation marks and any character can be present within the string
        elif re.fullmatch("\".*\"", curr_token):
                return TokenType.STRING_CONST
        else: 
            raise Exception(f"No token type could be matched for {curr_token}")

    def keyword(self) -> (Keyword, str):
        keyword_type = None
        match self.tokens[0]:
            case "class":
                keyword_type = Keyword.CLASS
            case "constructor":
                keyword_type = Keyword.CONSTRUCTOR
            case "function":
                keyword_type = Keyword.FUNCTION
            case "method":
                keyword_type = Keyword.METHOD
            case "field":
                keyword_type = Keyword.FIELD
            case "static":
                keyword_type = Keyword.STATIC
            case "var":
                keyword_type = Keyword.VAR
            case "int":
                keyword_type = Keyword.INT
            case "char":
                keyword_type = Keyword.CHAR
            case "boolean":
                keyword_type = Keyword.BOOLEAN
            case "void":
                keyword_type = Keyword.VOID
            case "true":
                keyword_type = Keyword.TRUE
            case "false":
                keyword_type = Keyword.FALSE
            case "null":
                keyword_type = Keyword.NULL
            case "this":
                keyword_type = Keyword.THIS
            case "let":
                keyword_type = Keyword.LET
            case "if":
                keyword_type = Keyword.IF
            case "else":
                keyword_type = Keyword.ELSE
            case "while":
                keyword_type = Keyword.WHILE
            case "return":
                keyword_type = Keyword.RETURN
            case "do":
                keyword_type = Keyword.DO
            case _:
                raise Exception(f"Invalid keyword \"{self.tokens[0]}\"")
        return (keyword_type, self.tokens[0])

    def symbol(self) -> str:
        if self.token_type() != TokenType.SYMBOL:
            raise Exception("Current token is not of type SYMBOL")
        else:
            return self.tokens[0]

    def identifier(self) -> str:
        if self.token_type() != TokenType.IDENTIFIER:
            raise Exception("Current token is not of type IDENTIFIER")
        else:
            return self.tokens[0]

    def int_val(self) -> int:
        if self.token_type() != TokenType.INT_CONST:
            raise Exception("Current token is not of type INT_CONST")
        else:
            return self.tokens[0]

    def string_val(self) -> str:
        if self.token_type() != TokenType.STRING_CONST:
            raise Exception("Current token is not of type STRING_CONST")
        else:
            return self.tokens[0].replace("\"", "")
