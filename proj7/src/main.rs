// Project 7: VM Translator (1)
// Vincent Nguyen
mod parser;
mod translator;
mod instr;
mod asmwriter;

use std::{env::args, fs::{exists, remove_file}};

use asmwriter::CodeWriter;
use instr::CommandType;
use parser::Parser;
use translator::Translator;

fn main() 
{
    // Get args
    let args: Vec<String> = args().collect();

    if args.len() < 2 { panic!("Not enough arguments provided"); }

    let input_file_path: &String = &args[1];
    let split_in_path: Vec<&str> = input_file_path.split(".").collect::<Vec<&str>>();
    let output_file_path: String = split_in_path[..split_in_path.len() - 1].to_vec().join("") + ".asm";
    if exists(&output_file_path).unwrap() { remove_file(&output_file_path).unwrap(); }

    // Initialize modules module
    let mut parser: Parser = Parser::new(input_file_path);
    let mut translator: Translator = Translator::init();
    let code_writer: CodeWriter  = CodeWriter::new(&output_file_path);

    while parser.has_more_commands()
    {
        code_writer.write_comment(&parser.get_command());

        if matches!(parser.get_command_type(), CommandType::ARITHMETIC)
        {
            code_writer.write_code(translator.translate_arithmetic(&parser.get_arg_1()));
        }
        else if matches!(parser.get_command_type(), CommandType::PUSH) || matches!(parser.get_command_type(), CommandType::POP)
        {
            code_writer.write_code(translator.translate_push_pop_code(&parser.get_command_type(), &parser.get_arg_1(), &parser.get_arg_2()));
        }

        parser.advance();
    }
}
