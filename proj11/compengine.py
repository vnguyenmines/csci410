import os
import xml.etree.ElementTree as xml_et
from language import Keyword, TokenType, ValType
from tokenizer import JackTokenizer
from vmwriter import VMWriter
from symboltable import SymbolTable

var_segment_type = {
    "var": "local",
    "arg": "argument",
    "field": "this",
    "static": "static"
}

class CompilationEngine:
    def __init__(self, input_file_path, output_xml_file_path, output_vm_file_path):
        self.input_path = input_file_path
        self.output_xml_path = output_xml_file_path
        # if os.path.exists(output_file_path):
        #     os.remove(output_file_path)
        self.tokenizer = JackTokenizer(input_file_path)
        self.vm_writer = VMWriter(output_vm_file_path)
        self.symbol_table = SymbolTable()
        self.label_count = 0
        self.class_name = None

    def compile_class(self):
        if self.tokenizer.has_more_tokens():
            # Class declaration
            self.class_root = xml_et.Element("class")
            # Class keyword
            CompilationEngine.__xml_token(self.class_root, "keyword", self.tokenizer.keyword()[1])
            self.tokenizer.advance()

            # Class identifier
            CompilationEngine.__xml_token(self.class_root, "identifier", self.tokenizer.identifier())
            self.class_name = self.tokenizer.identifier()
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
        var_kind = self.tokenizer.keyword()[1]
        self.tokenizer.advance()

        # Compiling the type and var name
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            CompilationEngine.__xml_token(var_root, "keyword", self.tokenizer.keyword()[1])
            var_type = self.tokenizer.keyword()[1]
            self.tokenizer.advance()
        # Data type
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()

        # var identifier
        CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
        var_name = self.tokenizer.identifier()
        self.tokenizer.advance()

        self.symbol_table.define(var_name, var_type, var_kind)

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
        self.symbol_table.start_subroutine()
        # Subroutine keyword
        CompilationEngine.__xml_token(subroutine_root, "keyword", self.tokenizer.keyword()[1])
        subroutine_type = self.tokenizer.keyword()[1]
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
        subroutine_name = self.tokenizer.identifier()
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
        # SYMBOL_TABLE: METHOD
        if subroutine_type == "method":
            self.symbol_table.define("this", self.class_name, "arg")
        # vars
        local_c = 0
        while self.tokenizer.keyword()[1] == "var":
            local_c += self.compile_var_dec(subroutine_body)
        # VM_OUT: Function
        self.vm_writer.write_function(self.class_name, subroutine_name, local_c)
        # VM_OUT: Constructor
        if subroutine_type == "constructor":
            self.vm_writer.write_push("constant", self.symbol_table.var_count(ValType.FIELD))
            self.vm_writer.write_call("Memory", "alloc", 1)
            self.vm_writer.write_pop("pointer", 0)
        # VM_OUT: METHOD
        if subroutine_type == "method":
            self.vm_writer.write_push("argument", 0)
            self.vm_writer.write_pop("pointer", 0)

        # statements
        self.compile_statements(subroutine_body)
        # ending symbol }
        CompilationEngine.__xml_token(subroutine_body, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

    def compile_parameter_list(self, function_root) -> int:
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

        var_c = 1

        # var keyword
        CompilationEngine.__xml_token(var_root, "keyword", self.tokenizer.keyword()[1])
        var_type = self.tokenizer.keyword()[1]
        self.tokenizer.advance()

        # Compiling the type and var name
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            CompilationEngine.__xml_token(var_root, "keyword", self.tokenizer.keyword()[1])
            var_type = self.tokenizer.keyword()[1]
            self.tokenizer.advance()
        # Data type
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
            var_type = self.tokenizer.identifier()
            self.tokenizer.advance()

        # var identifier
        CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
        var_name = self.tokenizer.identifier()
        self.tokenizer.advance()

        self.symbol_table.define(var_name, var_type, "var")

        # Multiple variables defined in one line
        while self.tokenizer.symbol() == ",":
            CompilationEngine.__xml_token(var_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            CompilationEngine.__xml_token(var_root, "identifier", self.tokenizer.identifier())
            self.tokenizer.advance()
            var_c += 1

        # closing symbol ;
        CompilationEngine.__xml_token(var_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        return var_c

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

            # self.vm_writer.
            self.vm_writer.write_arithmetic("add")

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
        arg_c = 0

        # do keyword
        CompilationEngine.__xml_token(do_statement_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # subroutine to call
        CompilationEngine.__xml_token(do_statement_root, "identifier", self.tokenizer.identifier())
        first_ident = self.tokenizer.identifier()
        self.tokenizer.advance()

        # dot operator
        if self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ".":
            CompilationEngine.__xml_token(do_statement_root, "symbol", self.tokenizer.symbol())
            self.tokenizer.advance()
            CompilationEngine.__xml_token(do_statement_root, "identifier", self.tokenizer.identifier())
            inner_ident = self.tokenizer.identifier()
            self.tokenizer.advance()

            do_type = self.symbol_table.type_of(first_ident)
            if do_type != None:
                self.push_var(first_ident)
                full_func_name = (do_type, inner_ident)
                arg_c = 1
            else:
                full_func_name = (first_ident, inner_ident)
        else:
            full_func_name = (self.class_name, first_ident)
            self.vm_writer.write_push("pointer", 0)
            arg_c = 1

        # opening symbol (
        CompilationEngine.__xml_token(do_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        # expression
        arg_c += self.compile_expression_list(do_statement_root)
        # closing symbol )
        CompilationEngine.__xml_token(do_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # ending symbol ;
        CompilationEngine.__xml_token(do_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.vm_writer.write_call(full_func_name[0], full_func_name[1], arg_c)
        self.vm_writer.write_pop("temp", 0)

    def compile_while(self, root):
        while_statement_root = xml_et.SubElement(root, "whileStatement")
        while_id = self.__hash_label("while")
        while_start_lbl = while_id + ".start"
        while_end_lbl = while_id + ".end"

        # while keyword
        CompilationEngine.__xml_token(while_statement_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()
        self.vm_writer.write_label(while_start_lbl)

        # start symbol (
        CompilationEngine.__xml_token(while_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        # expression eval
        self.compile_expression(while_statement_root)
        # end symbol )
        CompilationEngine.__xml_token(while_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if(while_end_lbl)
        
        # beginning {
        CompilationEngine.__xml_token(while_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        # statements
        self.compile_statements(while_statement_root)

        # ending }
        CompilationEngine.__xml_token(while_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()
        
        self.vm_writer.write_goto(while_start_lbl)
        self.vm_writer.write_label(while_end_lbl)

    def compile_if(self, root):
        if_statement_root = xml_et.SubElement(root, "ifStatement")
        if_id = self.__hash_label("if")
        if_true_lbl = if_id + ".start"
        if_end_lbl = if_id + ".end"

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

        self.vm_writer.write_if(if_true_lbl)
        self.vm_writer.write_goto(if_end_lbl)
        self.vm_writer.write_label(if_true_lbl)

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
        
        self.vm_writer.write_label(if_end_lbl)

    def compile_return(self, root):
        return_statement_root = xml_et.SubElement(root, "returnStatement")

        # return keyword
        CompilationEngine.__xml_token(return_statement_root, "keyword", self.tokenizer.keyword()[1])
        self.tokenizer.advance()

        # additional expressions
        if self.tokenizer.token_type() != TokenType.SYMBOL or self.tokenizer.symbol() != ";":
            self.compile_expression(return_statement_root)
        else:
            self.vm_writer.write_int(0)

        # ending ;
        CompilationEngine.__xml_token(return_statement_root, "symbol", self.tokenizer.symbol())
        self.tokenizer.advance()

        self.vm_writer.write_return()

    def compile_expression(self, root):
        expression_root = xml_et.SubElement(root, "expression")

        self.compile_term(expression_root)
        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            CompilationEngine.__xml_token(expression_root, "symbol", self.tokenizer.symbol())
            operation = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term(expression_root)

            match operation:
                case "+":
                    self.vm_writer.write_arithmetic("add")
                case "-":
                    self.vm_writer.write_arithmetic("sub")
                case "*":
                    self.vm_writer.write_call("Math", "multiply", 2)
                case "/":
                    self.vm_writer.write_call("Math", "divide", 2)
                case "&":
                    self.vm_writer.write_arithmetic("and")
                case "|":
                    self.vm_writer.write_arithmetic("or")
                case "<":
                    self.vm_writer.write_arithmetic("lt")
                case ">":
                    self.vm_writer.write_arithmetic("gt")
                case "=":
                    self.vm_writer.write_arithmetic("eq")

    def compile_term(self, root):
        term_root = xml_et.SubElement(root, "term")

        match self.tokenizer.token_type():
            case TokenType.KEYWORD:
                CompilationEngine.__xml_token(term_root, "keyword", self.tokenizer.keyword()[1])
                if self.tokenizer.keyword()[1] == "this":
                    self.vm_writer.write_push("pointer", 0)
                else:
                    self.vm_writer.write_int(0)
                    if self.tokenizer.keyword()[1] == "true":
                        self.vm_writer.write_arithmetic("not")
                self.tokenizer.advance()
            case TokenType.INT_CONST:
                CompilationEngine.__xml_token(term_root, "integerConstant", self.tokenizer.int_val())
                self.vm_writer.write_int(self.tokenizer.int_val())
                self.tokenizer.advance()
            case TokenType.STRING_CONST:
                CompilationEngine.__xml_token(term_root, "stringConstant", self.tokenizer.string_val())
                self.vm_writer.write_string(self.tokenizer.string_val())
                self.tokenizer.advance()
            case TokenType.SYMBOL:
                if self.tokenizer.symbol() == "(":
                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                    self.compile_expression(term_root)
                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                elif self.tokenizer.symbol() in ["~", "-"]:
                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    sym = self.tokenizer.symbol()
                    self.tokenizer.advance()
                    self.compile_term(term_root)
                    if sym == "-":
                        self.vm_writer.write_arithmetic("neg")
                    elif sym == "~":
                        self.vm_writer.write_arithmetic("not")
                    else:
                        raise Exception("Unreachable code")
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

                    # TODO: fix
                    self.push_var(prev_val)
                    self.vm_writer.write_arithmetic("add")
                    self.vm_writer.write_pop("pointer", 1)
                    self.vm_writer.write_pop("that", 0)

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
                    inner_ident = self.tokenizer.identifier()
                    self.tokenizer.advance()

                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()

                    arg_c = 0
                    subroutine_type = self.symbol_table.type_of(prev_val)
                    if subroutine_type != None:
                        self.push_var(prev_val)
                        full_func_name = (subroutine_type, inner_ident)
                        arg_c = 1
                    else:
                        full_func_name = (prev_val, inner_ident)

                    arg_c += self.compile_expression_list(term_root)

                    CompilationEngine.__xml_token(term_root, "symbol", self.tokenizer.symbol())
                    self.tokenizer.advance()
                    
                    self.vm_writer.write_call(full_func_name[0], full_func_name[1], arg_c)
                    self.vm_writer.write_pop("temp", 0)
                elif prev_is_identifier:
                    CompilationEngine.__xml_token(term_root, "identifier", prev_val) 
                elif self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == "(":
                    self.tokenizer.advance()

    def compile_expression_list(self, root):
        expression_list_root = xml_et.SubElement(root, "expressionList")

        expr_c = 0
        
        if self.tokenizer.token_type() != TokenType.SYMBOL or (self.tokenizer.token_type() == TokenType.SYMBOL and  self.tokenizer.symbol() != ")"):
            self.compile_expression(expression_list_root)
            expr_c += 1
            while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ",":
                CompilationEngine.__xml_token(expression_list_root, "symbol", self.tokenizer.symbol())
                self.tokenizer.advance()
                self.compile_expression(expression_list_root)
                expr_c += 1
        if self.tokenizer.symbol() == "(":
            self.compile_expression_list(expression_list_root)
            while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ",":
                CompilationEngine.__xml_token(expression_list_root, "symbol", self.tokenizer.symbol())
                self.tokenizer.advance()
                self.compile_expression(expression_list_root)

        return expr_c

    def push_var(self, identifier: str):
        kind = self.symbol_table.kind_of(identifier)
        index = self.symbol_table.index_of(identifier)
        self.vm_writer.write_push(var_segment_type[kind], index)

    def output_tokenized_parsed_code(self):
        tree = xml_et.ElementTree(self.class_root)
        xml_et.indent(tree, space="\t", level = 0)
        os.makedirs(os.path.dirname(self.output_xml_path), exist_ok=True)
        tree.write(self.output_xml_path, encoding="utf-8", xml_declaration=False, short_empty_elements=False)

    def output_vm_code(self):
        self.vm_writer.write_vm_file()

    def __xml_token(root, tag: str, value: str):
        element = xml_et.SubElement(root, tag)
        element.text = value
        return element
    
    def __hash_label(self, label) -> str:
        label_to_hash = str(label + str(self.label_count))
        # hash_val = "{}_{}".format(label, str(hash(label_to_hash)))
        hash_val = "{}_{}".format(self.class_name, str(self.label_count))
        self.label_count += 1
        return hash_val