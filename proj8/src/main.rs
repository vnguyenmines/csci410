// Project 7: VM Translator (1)
// Vincent Nguyen
mod parser;
mod translator;
mod instr;
mod asmwriter;

use std::{collections::HashMap, env::args, fs::{exists, remove_file}, path::Path};

use asmwriter::CodeWriter;
use instr::CommandType;
use parser::Parser;
use translator::Translator;

fn main() 
{
    // Get args
    let args: Vec<String> = args().collect();

    if args.len() < 2 { panic!("Not enough arguments provided"); }

    let input_path: String = if args[1].chars().nth(args[1].len() - 1) == Some('/') { 
        let mut _a = args[1].clone();
        _a.replace_range(args[1].len() - 1.., ""); 
        _a
    } else { args[1].clone() };
    let path: &Path = Path::new(&input_path);
    // Directory with .vn and Sys.vm
    let output_file_path: String;
    let mut vm_files: Vec<String> = Vec::new();
    if path.is_dir() 
    {
        path
            .read_dir()
            .unwrap()
            .for_each(|x: Result<std::fs::DirEntry, std::io::Error>| {
                let name: String = x.unwrap().file_name().into_string().unwrap().trim().to_string();
                if name[name.len() - 3..].to_owned() == ".vm" { vm_files.push(name); }
            });
        let split_in_path: Vec<&str> = input_path.split("/").collect::<Vec<&str>>();

        output_file_path = split_in_path.join("/") + "/" + split_in_path[split_in_path.len() - 1] + ".asm";
    }
    // Single file
    else if path.is_file()
    {
        vm_files.push(input_path.clone());
        let split_in_path: Vec<&str> = input_path.split(".").collect::<Vec<&str>>();
        output_file_path = split_in_path[..split_in_path.len() - 1].to_vec().join("") + ".asm"
    }
    else
    {
        panic!("Invalid path passed in");
    }

    // Validate the Sys.vm presence
    if path.is_dir() && (vm_files.len() > 1 && !vm_files.contains(&"Sys.vm".to_string()))
    {
        panic!("Multiple files specified in argument but no Sys.vm was specified");
    }
    if path.is_dir() && vm_files.len() == 0
    {
        panic!("No files found in argument passed in");
    }

    if exists(&output_file_path).unwrap() { remove_file(&output_file_path).unwrap(); }

    // Initialize modules module
    let code_writer: CodeWriter  = CodeWriter::new(&output_file_path);
    let mut parsers: HashMap<String, Parser> = HashMap::new();
    if path.is_dir() 
    {
        vm_files.iter().for_each(|x| { 
            parsers.insert(x.clone(), Parser::new(&format!("{}/{}", 
                &path.as_os_str()
                .to_str()
                .unwrap()
            , x.clone()))); 
        });
    }
    else if path.is_file() 
    {
        let _a = input_path.clone().split("/").map(|x| x.to_string()).collect::<Vec<String>>();
        parsers.insert(_a.get(_a.len() - 1).unwrap().to_string(), Parser::new(&input_path));
    }
    else 
    {
        panic!("Invalid invalid parser init");
    }
    
    let mut comment_new_line = false;
    let mut translator: Translator = Translator::init();

    let mut files: Vec<String> = parsers.keys().map(|x| x.to_string()).collect();
    if path.is_dir()
    {
        // Bootstrap code
        code_writer.write_code(translator.sys_init());
        files.sort();
        files.retain(|x| *x != "Sys.vm");
        files.push("Sys.vm".to_string());
    }

    for f_name in files
    {
        let current_parser: &mut Parser = parsers.get_mut(&f_name).unwrap();

        while current_parser.has_more_commands()
        {
            code_writer.write_comment(&current_parser.get_command(), comment_new_line);
            comment_new_line = true;

            match current_parser.get_command_type()
            {
                CommandType::ARITHMETIC => {
                    code_writer.write_code(translator.translate_arithmetic(&current_parser.get_arg_1()));
                },
                CommandType::PUSH | CommandType::POP => {
                    code_writer.write_code(translator.translate_push_pop_code(&current_parser.get_command_type(), &current_parser.get_arg_1(), &current_parser.get_arg_2()));
                },
                CommandType::LABEL => {
                    code_writer.write_code(translator.translate_label(&current_parser.get_arg_1()));
                },
                CommandType::GOTO => {
                    code_writer.write_code(translator.translate_goto(&current_parser.get_arg_1()));
                },
                CommandType::IF => {
                    code_writer.write_code(translator.translate_if(&current_parser.get_arg_1()));
                },
                CommandType::FUNCTION => {
                    // arg1: function name
                    // arg2: number of vars
                    code_writer.write_code(translator.translate_function(&current_parser.get_arg_1(), u32::try_from(current_parser.get_arg_2()).expect("Invalid argument count")));
                },
                CommandType::CALL => {
                    // arg1: function name
                    // arg2: number of vars
                    code_writer.write_code(translator.translate_call(&current_parser.get_arg_1(), u32::try_from(current_parser.get_arg_2()).expect("Invalid argument count")));
                },
                CommandType::RETURN => {
                    code_writer.write_code(translator.translate_return());
                }
            }
        
            current_parser.advance();
        }
    }
}
