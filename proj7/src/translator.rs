use core::panic;
use std::vec;

use crate::instr::CommandType;

pub struct Translator
{
    lbl_num: u32
}

impl Translator 
{
    pub fn init() -> Self
    {
        Self {
            lbl_num: 0
        }
    }

    // Write assembly code the is the translation of the arithmetic command
    pub fn translate_arithmetic(&mut self, arg: &String) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();
    
        match arg.as_str()
        {
            op @ ("add" | "sub" | "and" | "or") => {
                code.extend(vec![
                    // Load stack into Data register
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    // Look at next spot in stack (Stack[-1])
                    "@SP",
                    "A=M-1",
                ].iter().map(|x| x.to_string()));

                // Perform operation
                match op
                {
                    "add" => code.push("M=D+M".to_string()),
                    "sub" => code.push("M=M-D".to_string()),
                    "and" => code.push("M=D&M".to_string()),
                    "or" => code.push("M=D|M".to_string()),
                    _ => panic!("Unexpected error matching arithmetic op")
                }
            },
            op @ ("neg" | "not") => {
                code.extend(vec![
                    // Look at next spot in stack (Stack[-1])
                    "@SP",
                    "A=M-1"
                ].iter().map(|x| x.to_string()));

                // Perform operation
                match op
                {
                    "neg" => code.push("M=-M".to_string()),
                    "not" => code.push("M=!M".to_string()),
                    _ => panic!("Unexpected error matching arithmetic op")
                }
            },
            op @ ("eq" | "gt" | "lt") => {
                code.extend(vec![
                    // Load stack into Data register
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    // Look at next spot in stack (Stack[-1])
                    "@SP",
                    "A=M-1",
                    "D=M-D",
                    "M=-1",
                ].iter().map(|x| x.to_string()));

                let mut compare_asm_block: Vec<String> = Vec::new();

                let comparison_label: String = format!("LBL{}", self.lbl_num);
                compare_asm_block.append(&mut vec![
                    // jmp to label
                    format!("@{}", &comparison_label),
                    format!("D;{}", match op {
                        "lt" => "JLT",
                        "eq" => "JEQ",
                        "gt" => "JGT",
                        _ => panic!("Unexpected error")
                    }),

                    // comparison failure
                    String::from("@SP"),
                    String::from("A=M-1"),
                    String::from("M=0"),

                    // comparison success
                    format!("({})", &comparison_label),
                ]);

                self.lbl_num += 1;

                code.extend(compare_asm_block);
            }
            _ => panic!("Invalid arithmetic instruction - Arg provided: {arg}")
        }
        
        code
    }
    
    // Write assembly code that is the translation of the given push/pop command
    pub fn translate_push_pop_code(&self, cmd_type: &CommandType, seg: &String, index: &i32) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();

        // push/pop commands
        match cmd_type
        {
            CommandType::PUSH => {
                // segment
                match seg.as_str() 
                {
                    "constant" => {
                        code.extend([
                            format!("@{}", index).as_str(),
                            "D=A",
                            // Load stack into Data register
                            "@SP",
                            "AM=M+1",
                            "A=A-1",
                            // Added data to the stack
                            "M=D",
                        ].iter().map(|x| x.to_string()));
                    },
                    op @ ("this" | "that" | "argument" | "local" | "pointer" | "temp") => {
                        code.extend([
                            // Set the Data register to the index
                            format!("@{}", index).as_str(),
                            "D=A",
                            // Set the Address register to the index value
                            format!("@{}",
                                match op
                                {
                                    "this" => "THIS",
                                    "that" => "THAT",
                                    "argument" => "ARG",
                                    "local" => "LCL",
                                    "pointer" => "3",
                                    "temp" => "5",
                                    _ => panic!("Invalid segment")
                                }
                            ).as_str(),
                            if op != "pointer" && op != "temp"
                            {
                                "A=M"
                            }
                            else
                            {
                                ""
                            },
                            // Set the Address register to the source memory address of the value
                            "A=D+A",
                            "D=M",
                            "@SP",
                            "A=M",
                            "M=D",
                            "@SP",
                            "M=M+1"
                        ].iter().filter(|x: &&&str| !x.is_empty()).map(|x| x.to_string()));
                    },
                    "static" => {
                        code.extend([
                            // Create the static variable
                            format!("@STATIC_{}", index).as_str(),
                            "D=M",
                            "@SP",
                            "A=M",
                            "M=D",
                            "@SP",
                            "M=M+1",
                        ].iter().map(|x| x.to_string()));
                    },
                    _ => panic!("Invalid push command {}", seg)
                }

            },
            CommandType::POP => {
                // segment
                match seg.as_str() 
                {
                    "constant" => panic!("A constant segment cannot be popped"),
                    op @ ("this" | "that" | "argument" | "local" | "pointer" | "temp") => {
                        code.extend([
                            // Set the Data register to the index
                            format!("@{}", index).as_str(),
                            "D=A",
                            // Set the Address register to the index value
                            format!("@{}",
                                match op
                                {
                                    "this" => "THIS",
                                    "that" => "THAT",
                                    "argument" => "ARG",
                                    "local" => "LCL",
                                    "pointer" => "R3",
                                    "temp" => "R5",
                                    _ => panic!("Invalid segment")
                                }
                            ).as_str(),
                            if op != "temp" && op != "pointer"
                            {
                                "A=M"
                            }
                            else
                            {
                                ""
                            },
                            // Set the Data register to the source memory address of the value
                            "D=D+A",
                            // Store the source memory location into a register
                            "@R10",
                            "M=D",
                            // Set the Data register to the current value of the element at the top of the stack
                            "@SP",
                            "AM=M-1",
                            "D=M",
                            // Save the value into the respective register
                            "@R10",
                            "A=M",
                            "M=D",
                        ].iter().filter(|x: &&&str| !x.is_empty()).map(|x| x.to_string()));
                    },
                    "static" => {
                        code.extend([
                            // Set the Data register to the current value of the element at the top of the stack
                            "@SP",
                            "AM=M-1",
                            "D=M",
                            // Create the static variable
                            format!("@STATIC_{}", index).as_str(),
                            "M=D",
                        ].iter().map(|x| x.to_string()));
                    },
                    _ => panic!("Invalid pop command {}", seg)
                }
            },
            _ => { unimplemented!("Remaining functions are unimplemented"); }
        }

        code
    }
    
}
