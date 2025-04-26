# Project 10/11
# Vincent Nguyen
import sys
import xml.etree.ElementTree as xml_et
from tokenizer import JackTokenizer
from language import TokenType

# Instead of JackAnalyzer, we are using this main function to invoke JackTokenizer and CompilationEngine
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid arguments")
        exit()

    # Get file to compile
    file_name = sys.argv[1]

    # Tokenizer
    TOKENIZER = JackTokenizer(file_name)

    # TODO: CompilationEngine

    # Output to file
    root = xml_et.Element("token")
    while TOKENIZER.has_more_tokens():
        # Convert enum type to string and get the token value
        stringified_type = None
        token_value = None
        match TOKENIZER.token_type():
            case TokenType.KEYWORD:
                stringified_type = "keyword"
                (_, token_value) = TOKENIZER.keyword()
            case TokenType.SYMBOL:
                stringified_type = "symbol"
                token_value = TOKENIZER.symbol()
            case TokenType.IDENTIFIER:
                stringified_type = "identifier"
                token_value = TOKENIZER.identifier()
            case TokenType.INT_CONST:
                stringified_type = "integerConstant"
                token_value = TOKENIZER.int_val()
            case TokenType.STRING_CONST:
                stringified_type = "stringConstant"
                token_value = TOKENIZER.string_val()
            case _:
                print("invalid")

        # Error checking
        if stringified_type == None and token_value == None: raise Exception("Invalid token type output to XML")
        
        token = xml_et.SubElement(root, stringified_type)
        token.text = str(token_value)

        TOKENIZER.advance()

    tree = xml_et.ElementTree(root)
    xml_et.indent(tree, space="", level = 0)
    tree.write("out.xml", encoding="utf-8", xml_declaration=False)