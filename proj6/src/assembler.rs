use std::{collections::BTreeMap, fs::read_to_string};

pub struct Assembler
{
    raw_code: String,
    variable_stack_ptr: u32,
    label_table: BTreeMap<String, u32>,
    comp_table: BTreeMap<String, String>,
    dest_table: BTreeMap<String, String>,
    jump_table: BTreeMap<String, String>,
}

impl Assembler {
    pub fn new(code: &String) -> Self
    {
        // label table
        let mut init_lbl_table: BTreeMap<String, u32> = BTreeMap::from([
            (String::from("SP"), 0),
            (String::from("LCL"), 1),
            (String::from("ARG"), 2),
            (String::from("THIS"), 3),
            (String::from("THAT"), 4),
            (String::from("SCREEN"), 16384),
            (String::from("KBD"), 24576),
        ]);

        for x in 0..16
        {
            init_lbl_table.insert(format!("R{x}"), x);
        }

        // comp table
        let comp_file_contents: String = read_to_string("src/comp.txt").expect("Not found comp.txt");
        let mut comp_rules: BTreeMap<String, String> = BTreeMap::new();
        for x in comp_file_contents.split("\n").collect::<Vec<&str>>().iter().map(|x: &&str| {
            let t: Vec<&str>  = x.split_whitespace().collect();
            (t[0].to_string(), t[1].to_string())
        }).collect::<Vec<(String, String)>>()
        {
            comp_rules.insert(x.0.to_string(), x.1.to_string());
        }

        // dest table
        let dest_file_contents: String = read_to_string("src/dest.txt").expect("Not found dest.txt");
        let mut dest_rules: BTreeMap<String, String> = BTreeMap::new();
        for x in dest_file_contents.split("\n").collect::<Vec<&str>>().iter().map(|x: &&str| {
            let t: Vec<&str>  = x.split_whitespace().collect();
            (t[0].to_string(), t[1].to_string())
        }).collect::<Vec<(String, String)>>()
        {
            dest_rules.insert(x.0.to_string(), x.1.to_string());
        }

        // jump table
        let jump_file_contents: String = read_to_string("src/jump.txt").expect("Not found dest.txt");
        let mut jump_rules: BTreeMap<String, String> = BTreeMap::new();
        for x in jump_file_contents.split("\n").collect::<Vec<&str>>().iter().map(|x: &&str| {
            let t: Vec<&str>  = x.split_whitespace().collect();
            (t[0].to_string(), t[1].to_string())
        }).collect::<Vec<(String, String)>>()
        {
            jump_rules.insert(x.0.to_string(), x.1.to_string());
        }


        return Self { 
            raw_code: code.clone(), 
            label_table: init_lbl_table,
            variable_stack_ptr: 16,
            comp_table: comp_rules,
            dest_table: dest_rules,
            jump_table: jump_rules,
        }
    }

    pub fn translate(&mut self) -> Vec<String>
    {
        // Format code into a more digestable form
        let formatted_code: Vec<String> = self.format_code(&self.raw_code);
        
        // First pass to log all labels
        let mut line_num: u32 = 0;
        for line in &formatted_code
        {
            if line.chars().collect::<Vec<char>>()[0] == '('
            {
                // Get label name
                let mut label: String = String::from("");
                let label_terminate_idx: Option<usize> = line.find(")");
                if label_terminate_idx.is_none() || label_terminate_idx.unwrap() >= line.len() { panic!("Invalid label {label}") }

                for c in line.chars()
                {
                    // Error checking
                    if c == '(' || c == ')'
                    {
                        continue;
                    }
                    else
                    {
                        label += &c.to_string();
                    }
                }
                
                self.label_table.insert(label.to_owned(), line_num);
            }
            else
            {
                line_num += 1;
            }
        }

        let mut bin_code: Vec<String> = Vec::new();

        // Second pass
        line_num = 1;
        for line in &formatted_code
        {
            if line.chars().nth(0).unwrap() == '(' { continue }

            // A-instruction
            bin_code.push(
                if line.chars().nth(0).expect(&format!("Empty line bypassed")) == '@' && line.chars().nth(1).expect(&format!("Invalid character found at {}", line_num)).is_alphabetic()
                {
                    let var_name: &str = &line[1..];

                    if !self.label_table.contains_key(var_name)
                    {
                        self.label_table.insert(var_name.to_string(), self.variable_stack_ptr);
                        self.variable_stack_ptr += 1;
                    }

                    format!("{:016b}", self.label_table.get(&var_name.to_string()).unwrap())
                }
                else if line.chars().nth(0).expect(&format!("Empty line bypassed")) == '@'
                {
                    format!("{:016b}", line[1..].parse::<u32>().unwrap())
                }
                // C-instruction
                else
                {
                    let mut formatted_line: String = line.clone();
                    if !formatted_line.contains("=") 
                    { 
                        formatted_line = "null=".to_owned() + &formatted_line.to_owned();
                    }
                    else if !formatted_line.contains(";")
                    {
                        formatted_line = formatted_line.to_owned() + ";null";
                    }

                    let expr: Vec<&str> = formatted_line.split("=").collect();

                    // Destination
                    let dest_bits: &String = self.dest_table.get(expr.get(0).unwrap().to_owned()).expect("destfail");

                    let jmp_expr: Vec<&str> = expr[1].split(";").collect();

                    // Computation
                    let comp_bits = self.comp_table.get(jmp_expr.get(0).unwrap().to_owned()).expect("compfail");

                    // Jump
                    let jump_bits = self.jump_table.get(jmp_expr.get(1).unwrap().to_owned()).expect("compfail");

                    format!("111{}{}{}", comp_bits, dest_bits, jump_bits)
                }
            );
            
            line_num += 1;
        }

        return bin_code;
    }

    /// Format code by splitting it at new line characters 
    fn format_code(&self, code: &String) -> Vec<String>
    {
        let split_lines: Vec<String> = code.split("\n").into_iter().map(|s| s.trim().to_string()).collect();

        let mut cleaned_lines: Vec<String> = Vec::new();

        for i in 0..split_lines.len()
        {
            let curr_line: &String = &split_lines[i];

            let line_comment_idx: Option<usize> = curr_line.find("//");
            // Comment is at the beginning of the line
            if line_comment_idx.is_some() && line_comment_idx.unwrap() == 0 || curr_line == ""
            {
                continue;
            } 
            // Comment is towards the end of the line
            else if line_comment_idx.is_some()
            {
                cleaned_lines.push(curr_line.to_owned().chars().take(line_comment_idx.unwrap()).collect::<String>().trim().to_string());
            }
            else
            {
                cleaned_lines.push(curr_line.to_owned());
            }
        }

        return cleaned_lines;
    }
}



#[cfg(test)]
mod tests
{
    use crate::assembler::Assembler;

    #[test]
    fn slides_test()
    {
        let code: &str = 
"      @i
    M=1    // i = 1 
    @sum 
    M=0    // sum = 0 
(LOOP)					 
    @i     
    D=M     // D = i                             
    @100                                
    D=D-A   // D = i - 100                            
    @END
    D;JGT   // If (i-100) > 0 goto END                            
    @i                        
    D=M     // D = i                             
    @sum                                
    M=D+M   // sum += i                            
    @i                            
    M=M+1   // i++                             
    @LOOP
    0;JMP   // Goto LOOP                            
 (END)
    @END 
    0;JMP   // Infinite loop
";

        let mut asmblr = Assembler::new(&code.to_string());

        let translate_result = asmblr.translate();

        assert_eq!(translate_result.join("\n"), "0000000000010000
1110111111001000
0000000000010001
1110101010001000
0000000000010000
1111110000010000
0000000001100100
1110010011010000
0000000000010010
1110001100000001
0000000000010000
1111110000010000
0000000000010001
1111000010001000
0000000000010000
1111110111001000
0000000000000100
1110101010000111
0000000000010010
1110101010000111")
    }
}