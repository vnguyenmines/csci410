use std::collections::VecDeque;
use std::fs::read_to_string;
use crate::instr::CommandType;

pub struct Parser
{
    _parsed_code: VecDeque<Vec<String>>
}

impl Parser 
{
    pub fn new(vm_file_path: &String) -> Self
    {
        // Read in the VM IR code
        let vm_ir_code: String = read_to_string(vm_file_path).expect(&format!("Invalid file provided: {}", vm_file_path));

        // Parse the code file, removing any comments and empty lines
        let parsed_code: VecDeque<Vec<String>> = vm_ir_code.split('\n')
            .map(|l: &str| l.trim_end_matches('\r'))
            .filter(|l: &&str| !l.trim().starts_with("//"))
            .filter(|l| l.trim().len() > 0)
            .map(|l: &str| l.to_string().split_whitespace().map(|z| z.to_string()).collect::<Vec<String>>())
            .collect();

        return Self {
            _parsed_code: parsed_code
        };
    }

    /// Check if there are more commands in the input 
    pub fn has_more_commands(&self) -> bool
    {
        !self._parsed_code.is_empty()
    }
    
    /// Pops the queue and goes to the next command
    pub fn advance(&mut self)
    {
        self._parsed_code.pop_front();
    }

    /// Gets the current command
    pub fn get_command(&self) -> String
    {
        self._parsed_code
            .front().unwrap()
            .join(" ")
    }

    /// Retrieves the current command's type
    pub fn get_command_type(&self) -> CommandType
    {
        if self._parsed_code.is_empty() 
        { 
            panic!("Parsed code queue is empty"); 
        }

        match self._parsed_code[0][0].as_str()
        {
            "pop" => CommandType::POP,
            "push" => CommandType::PUSH,
            "add" | "sub" | "neg" | "eq" | "gt" | "lt" | "and" | "or" | "not" => CommandType::ARITHMETIC,
            _ => panic!("Invalid instruction at {}", self._parsed_code.front().unwrap().join(" "))
        }
    }

    // Retrieves the first argument of the current command
    pub fn get_arg_1(&self) -> String
    {
        if matches!(self.get_command_type(), CommandType::ARITHMETIC)
        {
            self._parsed_code
                .front().unwrap()
                .get(0).unwrap()
                .clone()
        }
        else 
        {
            self._parsed_code
                .front().unwrap()
                .get(1).unwrap()
                .clone()
        }
    }

    // Retrieves the second argument of the command. Only invoke if current command type is PUSH, POP, FUNCTION, or CALL
    pub fn get_arg_2(&self) -> i32
    {
        self._parsed_code
            .front().unwrap()
            .get(2).unwrap()
            .parse::<i32>().unwrap()
    }
}