# Project 10/11
# Vincent Nguyen
import sys
import os
import xml.etree.ElementTree as xml_et
from tokenizer import JackTokenizer
from language import TokenType
from compengine import CompilationEngine

OUTPUT_TOKENIZED_CODE = True

# Instead of JackAnalyzer, we are using this main function to invoke JackTokenizer and CompilationEngine
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid arguments")
        exit()

    # Input file path
    path_arg = sys.argv[1]
    jack_files = []
    if os.path.isdir(path_arg):
        # remove trailing slash /
        if path_arg[-1:] == "/":
            path_arg = path_arg[:-1]
        jack_files = list(filter(lambda x: x[-5:] == ".jack", os.listdir(path_arg)))

    # Tokenize and parse all Jack files
    for jack_file in jack_files:
        file_name = jack_file[:-5]
        # Output file path
        completed_output_name = os.path.join("out", "{}.xml".format(file_name))
        tokenized_output_name = os.path.join("{}T.xml".format(file_name))

        # Tokenizer
        if OUTPUT_TOKENIZED_CODE:
            TOKENIZER = JackTokenizer(os.path.join(path_arg, jack_file))

            # Output to file
            root = xml_et.Element("tokens")
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

                # Error checking
                if stringified_type == None and token_value == None: raise Exception("Invalid token type output to XML")
                
                token = xml_et.SubElement(root, stringified_type)
                token.text = str(token_value)

                TOKENIZER.advance()

            tree = xml_et.ElementTree(root)
            xml_et.indent(tree, space="\t", level = 0)
            tree.write(tokenized_output_name, encoding="utf-8", xml_declaration=False)

        # Running through CompilationEngine
        engine = CompilationEngine(str(os.path.join(path_arg, jack_file)), completed_output_name)
        # Compile the class the file defines
        engine.compile_class()
        # Output XML
        engine.output_tokenized_parsed_code()