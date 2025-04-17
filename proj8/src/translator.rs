use core::panic;

use crate::instr::CommandType;

pub struct Translator
{
    lbl_num: u32,
    current_function: Option<String>,
}

impl Translator 
{
    pub fn init() -> Self
    {
        Self {
            lbl_num: 0,
            current_function: None,
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
                    "A=M",
                    "A=A-1",
                    "A=A-1",
                    "D=M",
                    "A=A+1",
                    "D=D-M",
                    // Look at next spot in stack (Stack[-1])
                    "@SP",
                    "M=M-1",
                    "M=M-1",
                ].iter().map(|x| x.to_string()));

                let mut compare_asm_block: Vec<String> = Vec::new();

                let comparison_label: String = format!("{}_{}", op.to_uppercase(), self.lbl_num);
                compare_asm_block.extend(vec![
                    // jmp to label when true case
                    format!("@{}", &comparison_label).as_str(),
                    format!("D;{}", match op {
                        "lt" => "JLT",
                        "eq" => "JEQ",
                        "gt" => "JGT",
                        _ => panic!("Unexpected error")
                    }).as_str(),

                    // comparison failure
                    "@SP",
                    "A=M",
                    "M=0",
                    format!("@END_{}", self.lbl_num).as_str(),
                    "0;JMP",

                    // comparison success
                    "",
                    format!("({})", &comparison_label).as_str(),
                    "@SP",
                    "A=M",
                    "M=-1",

                    // comparison fails
                    "",
                    format!("(END_{})", self.lbl_num).as_str(),
                    "@SP",
                    "M=M+1"
                ].iter().map(|x| x.to_string()).collect::<Vec<String>>());

                self.lbl_num += 1;

                code.extend(compare_asm_block);
            }
            _ => panic!("Invalid arithmetic instruction - Arg provided: {arg}")
        }
        
        code
    }
    
    // Write assembly code that is the translation of the given push/pop command
    pub fn translate_push_pop_code(&mut self, cmd_type: &CommandType, seg: &String, index: &i32) -> Vec<String>
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
                            "A=M",
                            // Added data to the stack
                            "M=D",
                            "@SP",
                            "M=M+1"
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
                            "D=D+A",
                            "A=D",
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
                            format!("@STATIC_{}_{}", index, self.current_function.clone().unwrap_or("none".to_string())).as_str(),
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
                            "M=D",
                            // Set the Data register to the current value of the element at the top of the stack
                            "@SP",
                            "M=M-1",
                            "A=M",
                            "D=M",
                            // Save the value into the respective register
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
                            "A=M",
                            "M=D",

                            format!("@{}", index).as_str(),
                            "D=A",
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
                            "A=M",
                            "D=A-D",
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
                            "M=D"
                        ].iter().filter(|x: &&&str| !x.is_empty()).map(|x| x.to_string()));
                    },
                    "static" => {
                        code.extend([
                            // Set the Data register to the current value of the element at the top of the stack
                            "@SP",
                            "AM=M-1",
                            "D=M",
                            // Create the static variable
                            format!("@STATIC_{}_{}", index, self.current_function.clone().unwrap_or("none".to_string())).as_str(),
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

    // Label translation
    pub fn translate_label(&self, label: &String) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();
        
        code.push(format!("({label})"));
        
        code
    }
    
    // Unconditional goto statements
    pub fn translate_goto(&self, label: &String) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();
        
        // Select the label to jump to
        code.push(format!("@{}", label));
        code.push(String::from("0;JMP"));

        code
    }
    
    // If statements
    pub fn translate_if(&self, label: &String) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();
        
        code.append(&mut vec![
            // Performs the comparison operation, pops the topmost value into register D from the stack 
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            // Select the label to jump to
            format!("@{}", label).as_str(),
            "D;JNE"
        ].iter().map(|x| x.to_string()).collect());

        code
    }

    // Functions
    pub fn translate_function(&mut self, fn_name: &String, _arg_c: u32) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();

        // Cleaning function name
        let mut cleaned_function_name: String = fn_name.clone();
        if fn_name.contains(".")
        {
            let period_index = cleaned_function_name.split("").into_iter().position(|x| x == ".").unwrap();
            cleaned_function_name = cleaned_function_name[..period_index - 1].to_string();
        }

        self.current_function = Some(cleaned_function_name.to_owned());

        code.push(format!("// Defining function {}", fn_name));
        code.extend(self.translate_label(fn_name));

        code
    }

    // When a Sys.init is present
    pub fn sys_init(&mut self) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();

        self.current_function = Some("Sys.init".to_string());

        code.extend([
            "// Boilerplate bootstrap for Sys.init. Call Sys.init, initalize stack point to 256",
            "@256",
            "D=A",
            "@SP",
            "M=D",
            "",
            "// Calling Sys.init 0"
        ].iter().map(|x| x.to_string()).collect::<Vec<String>>());

        code.extend(self.translate_call(&"Sys.init".to_string(), 0));   

        code
    }

    // Call
    pub fn translate_call(&mut self, fn_name: &String, arg_c: u32) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();
        
        code.extend([
            // Save all register states to the stack
            // Load function to call by pushing the return address
            format!("@FUNC_{}_{}_{}", fn_name, arg_c, self.lbl_num).as_str(),
            "D=A",
            // Push return address to stack
            "@SP",
            "A=M",
            "M=D",
            // Move stack forward
            "@SP",
            "M=M+1",
            // Push LCL
            "@LCL",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            // Push ARG
            "@ARG",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            // Push THIS
            "@THIS",
            "D=M",
            "@SP", 
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            // Push THAT
            "@THAT",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            // Reset ARG position
            "D=M",
            format!("@{}", arg_c).as_str(),
            "D=D-A",
            "@5",
            "D=D-A",
            // Reset stack pointer to the top
            "@ARG",
            "M=D",
            // Set the local register to the stack pointer
            "@SP",
            "D=M",
            "@LCL",
            "M=D",
            // Jump to function
            format!("@{}", fn_name).as_str(),
            "0;JMP",
            format!("(FUNC_{}_{}_{})", fn_name, arg_c, self.lbl_num).as_str()
        ].iter().map(|x| x.to_string()).collect::<Vec<String>>());

        self.lbl_num += 1;

        code
    }

    // Function return
    pub fn translate_return(&self) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();

        code.extend(vec![
            // Get LCL pointer
            "@LCL",
            "D=M",
            // Get the stack frame
            "@STACK_FRAME",
            "M=D",
            // RETURN = *(STACK_FRAME - 5)
            "@5",
            "D=D-A",
            "A=D",
            "D=M",
            "@RETURN",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            // pop = *ARGS 
            "@ARG",
            "A=M",
            "M=D",
            "@ARG",
            "D=M+1",
            // SP = ARGS + 1
            "@SP",
            "M=D",
            "@STACK_FRAME",
            "D=M",
            "@1",
            "D=D-A",
            "A=D",
            "D=M",
            // THAT = *(STACK_FRAME - 1) 
            &self.pop_variable_stack("STACK_FRAME", "THAT", 2).join("\n").to_owned(),
            // THIS = *(STACK_FRAME - 2) 
            &self.pop_variable_stack("STACK_FRAME", "THIS", 3).join("\n").to_owned(),
            // ARG = *(STACK_FRAME - 3) 
            &self.pop_variable_stack("STACK_FRAME", "ARG", 4).join("\n").to_owned(),
            // LCL = *(STACK_FRAME - 4)
            "@LCL",
            "M=D",
            "@RETURN",
            "A=M",
            "0;JMP"
        ].iter().map(|x| x.to_string()).collect::<Vec<String>>());

        code
    }

    // Updates a variable respectively stored in the stack
    fn pop_variable_stack(&self, src: &str, dest: &str, offset: u32) -> Vec<String>
    {
        let mut code: Vec<String> = Vec::new();
        
        code.extend(vec![
            format!("@{}", dest).as_str(),
            "M=D",
            format!("@{}", src).as_str(),
            "D=M",
            format!("@{}", offset).as_str(),
            "D=D-A",
            "A=D",
            "D=M",
        ].iter().map(|x| x.to_string()).collect::<Vec<String>>());

        code
    }

}
