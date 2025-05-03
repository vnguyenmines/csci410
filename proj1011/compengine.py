import os
import xml.etree.ElementTree as xml_et
from language import Keyword, TokenType
from tokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self, input_file_path, output_file_path):
        self.input_path = input_file_path
        self.output_path = output_file_path
        # if os.path.exists(output_file_path):
        #     os.remove(output_file_path)
        self.tokenizer = JackTokenizer(input_file_path)

    def compile_class(self):
        if self.tokenizer.has_more_tokens():
            # Class declaration
            self.class_root = xml_et.Element("class")
            # Class keyword
            CompilationEngine.__xml_token(self.class_root, "keyword", self.tokenizer.keyword()[1])
            self.tokenizer.advance()

            # Class identifier
            CompilationEngine.__xml_token(self.class_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()
            # Class symbol begin
            CompilationEngine.__xml_token(self.class_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()

            # Class declaration hierarchy Static -> Field -> Constructor -> Functions/Method(s)
            # Compile static/field variables
            while self.tokenizer.keyword()[0] == Keyword.STATIC or self.tokenizer.keyword()[0] == Keyword.FIELD:
                self.compile_class_var_declaration()
            while len(self.tokenizer.tokens) != 0 and self.tokenizer.token_type() != TokenType.SYMBOL and (self.tokenizer.keyword()[0] == Keyword.CONSTRUCTOR or self.tokenizer.keyword()[0] == Keyword.FUNCTION or self.tokenizer.keyword()[0] == Keyword.METHOD):
                self.compile_subroutine()

            # closing }
            CompilationEngine.__xml_token(self.class_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()

            if self.tokenizer.has_more_tokens():
                raise Exception("More tokens still present")

            self.output_tokenized_parsed_code()

    def compile_class_var_declaration(self):
        # Class var declaration
        var_root = xml_et.SubElement(self.class_root, "classVarDec")

        # var type
        CompilationEngine.__xml_token(var_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # Compiling the type and var name
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            CompilationEngine.__xml_token(var_root, "keyword", self.tokenizer.keyword()[1])
            self.tokenizer.advance()
        # Data type
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        # var identifier
        CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # Multiple variables defined in one line
        while self.tokenizer.symbol() == ",":
            CompilationEngine.__xml_token(var_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        # closing symbol ;
        CompilationEngine.__xml_token(var_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

    def compile_subroutine(self):
        # Subroutine declaration
        subroutine_root = xml_et.SubElement(self.class_root, "subroutineDec")
        # Subroutine keyword
        CompilationEngine.__xml_token(subroutine_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # Subroutine return type
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            CompilationEngine.__xml_token(subroutine_root, "keyword", self.tokenizer.keyword()[1])
            self.tokenizer.advance()
        # Subrouting ..
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            CompilationEngine.__xml_token(subroutine_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        # Subroutine identifier
        CompilationEngine.__xml_token(subroutine_root, "identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # Parameters
        # symbol begin (
        CompilationEngine.__xml_token(subroutine_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        # params
        self.compile_parameter_list(subroutine_root)
        # symbol end )
        CompilationEngine.__xml_token(subroutine_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # Subroutine body
        subroutine_body = xml_et.SubElement(subroutine_root, "subroutineBody")
        # starting symbol {
        CompilationEngine.__xml_token(subroutine_body, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        # vars
        while self.tokenizer.keyword()[1] == "var":
            self.compile_var_dec(subroutine_body)
        # statements
        self.compile_statements(subroutine_body)
        # ending symbol }
        CompilationEngine.__xml_token(subroutine_body, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

    def compile_parameter_list(self, function_root):
        # Parameter declaration
        params_root = xml_et.SubElement(function_root, "parameterList")

        # Build parameters
        while self.tokenizer.token_type() != TokenType.SYMBOL:
            # Keyword to define the type
            if self.tokenizer.token_type() == TokenType.KEYWORD:
                CompilationEngine.__xml_token(params_root, "keyword", self.tokenizer.keyword()[1])
                self.tokenizer.advance()
            # Parameter identifier
            elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
                CompilationEngine.__xml_token(params_root, "identifier", self.tokenizer.identifier())
                self.tokenizer.advance()
                
            CompilationEngine.__xml_token(params_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

            if self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ",":
                CompilationEngine.__xml_token(params_root, "symbol", self.tokenizer.symbol())
                self.tokenizer.advance()

    def compile_var_dec(self, root):
        var_root = xml_et.SubElement(root, "varDec")

        # var keyword
        CompilationEngine.__xml_token(var_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # Compiling the type and var name
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            CompilationEngine.__xml_token(var_root, "keyword", self.tokenizer.keyword()[1])
            self.tokenizer.advance()
        # Data type
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        # var identifier
        CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # Multiple variables defined in one line
        while self.tokenizer.symbol() == ",":
            CompilationEngine.__xml_token(var_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        # closing symbol ;
        CompilationEngine.__xml_token(var_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

    def compile_statements(self, root):
        # Statements declaration
        statement_root = xml_et.SubElement(root, "statements")
        # Statements
        while self.tokenizer.token_type() == TokenType.KEYWORD:
            match self.tokenizer.keyword()[0]:
                case Keyword.LET:
                    self.compile_let(statement_root)
                case Keyword.IF: 
                    self.compile_if(statement_root)
                case Keyword.DO:
                    self.compile_do(statement_root)
                case Keyword.WHILE:
                    self.compile_while(statement_root)
                case Keyword.RETURN:
                    self.compile_return(statement_root)
                case _:
                    raise Exception("Invalid keyword in compile_statements match-case")

    def compile_let(self, root):
        let_statement_root = xml_et.SubElement(root, "letStatement")

        # let keyword
        CompilationEngine.__xml_token(let_statement_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # identifier
        CompilationEngine.__xml_token(let_statement_root, "identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # array declaration
        if self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == "[":
            # starting symbol [
            CompilationEngine.__xml_token(let_statement_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            # evaluate expressions inside the array
            self.compile_expression(let_statement_root)
            # ending symbol ]
            CompilationEngine.__xml_token(let_statement_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()

        # equal symbol
        CompilationEngine.__xml_token(let_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # statement
        self.compile_expression(let_statement_root)
        
        # closing ;
        CompilationEngine.__xml_token(let_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

    def compile_do(self, root):
        do_statement_root = xml_et.SubElement(root, "doStatement")

        # do keyword
        CompilationEngine.__xml_token(do_statement_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # subroutine to call
        CompilationEngine.__xml_token(do_statement_root, "identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

        # dot operator
        if self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ".":
            CompilationEngine.__xml_token(do_statement_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            CompilationEngine.__xml_token(do_statement_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        # opening symbol (
        CompilationEngine.__xml_token(do_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        # expression
        self.compile_expression_list(do_statement_root)
        # closing symbol )
        CompilationEngine.__xml_token(do_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # ending symbol ;
        CompilationEngine.__xml_token(do_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()


    def compile_while(self, root):
        while_statement_root = xml_et.SubElement(root, "whileStatement")

        # while keyword
        CompilationEngine.__xml_token(while_statement_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # start symbol (
        CompilationEngine.__xml_token(while_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        # expression eval
        self.compile_expression(while_statement_root)
        # end symbol )
        CompilationEngine.__xml_token(while_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # beginning {
        CompilationEngine.__xml_token(while_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # statements
        self.compile_statements(while_statement_root)

        # ending }
        CompilationEngine.__xml_token(while_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        

    def compile_if(self, root):
        if_statement_root = xml_et.SubElement(root, "ifStatement")

        # if keyword
        CompilationEngine.__xml_token(if_statement_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # starting symbol (
        CompilationEngine.__xml_token(if_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance() 
        # expression eval
        self.compile_expression(if_statement_root)
        # ending symbol )
        CompilationEngine.__xml_token(if_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # starting symbol {
        CompilationEngine.__xml_token(if_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        # statements
        self.compile_statements(if_statement_root)
        # ending symbol }
        CompilationEngine.__xml_token(if_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        if self.tokenizer.token_type() == TokenType.KEYWORD and self.tokenizer.keyword()[0] == Keyword.ELSE:
            # else keyword
            CompilationEngine.__xml_token(if_statement_root, "keyword", self.tokenizer.keyword()[1])
            self.tokenizer.advance()
            # starting symbol {
            CompilationEngine.__xml_token(if_statement_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            # statements
            self.compile_statements(if_statement_root)
            # ending symbol }
            CompilationEngine.__xml_token(if_statement_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()

    def compile_return(self, root):
        return_statement_root = xml_et.SubElement(root, "returnStatement")

        # return keyword
        CompilationEngine.__xml_token(return_statement_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # additional expressions
        if self.tokenizer.token_type() != TokenType.SYMBOL or self.tokenizer.symbol() != ";":
            self.compile_expression(return_statement_root)

        # ending ;
        CompilationEngine.__xml_token(return_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()


    def compile_expression(self, root):
        expression_root = xml_et.SubElement(root, "expression")

        self.compile_term(expression_root)
        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            CompilationEngine.__xml_token(expression_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            self.compile_term(expression_root)

    def compile_term(self, root):
        term_root = xml_et.SubElement(root, "term")

        match self.tokenizer.token_type():
            case TokenType.KEYWORD:
                CompilationEngine.__xml_token(term_root, "keyword", self.tokenizer.keyword()[1])
                self.tokenizer.advance()
            case TokenType.INT_CONST:
                CompilationEngine.__xml_token(term_root, "integerConstant", self.tokenizer.int_val())
                self.tokenizer.advance()
            case TokenType.STRING_CONST:
                CompilationEngine.__xml_token(term_root, "stringConstant", self.tokenizer.string_val())
                self.tokenizer.advance()
            case TokenType.SYMBOL:
                if self.tokenizer.symbol() == "(":
                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                    self.compile_expression(term_root)
                elif self.tokenizer.symbol() in ["~", "-"]:
                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                    self.compile_term(term_root)
            case _:
                prev_val = self.tokenizer.curr_token()
                prev_is_identifier = self.tokenizer.token_type() == TokenType.IDENTIFIER

                self.tokenizer.advance()
                if self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == "[":
                    # identifier
                    CompilationEngine.__xml_token(term_root, "identifier", prev_val) 
                    # opening symbol [
                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                    # eval expression in the brackets
                    self.compile_expression(term_root)
                    # closing symbol ]
                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                elif self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ".":
                    # Class
                    CompilationEngine.__xml_token(term_root, "identifier", prev_val) 
                    # dot operator
                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                    # Subroutine call
                    CompilationEngine.__xml_token(term_root, "identifier", self.tokenizer.identifier())
                    self.tokenizer.advance()

                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()

                    self.compile_expression_list(term_root)

                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                elif prev_is_identifier:
                    CompilationEngine.__xml_token(term_root, "identifier", prev_val) 
                elif self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == "(":
                    self.tokenizer.advance()

    def compile_expression_list(self, root):
        expression_list_root = xml_et.SubElement(root, "expressionList")
        
        if self.tokenizer.token_type() != TokenType.SYMBOL or (self.tokenizer.token_type() == TokenType.SYMBOL and  self.tokenizer.symbol() != ")"):
            self.compile_expression(expression_list_root)
            while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ",":
                CompilationEngine.__xml_token(expression_list_root, "symbol", self.tokenizer.symbol())
                self.tokenizer.advance()
                self.compile_expression(expression_list_root)
        if self.tokenizer.symbol() == "(":
            self.compile_expression_list(expression_list_root)
            while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ",":
                CompilationEngine.__xml_token(expression_list_root, "symbol", self.tokenizer.symbol())
                self.tokenizer.advance()
                self.compile_expression(expression_list_root)

    def output_tokenized_parsed_code(self):
        tree = xml_et.ElementTree(self.class_root)
        xml_et.indent(tree, space="", level = 0)
        # xml_et.indent(tree, space="\t", level = 0)
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        os.
        if not os.path.exists(self.output_path):
            with open(self.output_path, "w+") as f:
                pass
        tree.write(self.output_path, encoding="utf-8", xml_declaration=False, short_empty_elements=False)

    def __xml_token(root, tag: str, value: str):
        element = xml_et.SubElement(root, tag)
        element.text = value
        return element