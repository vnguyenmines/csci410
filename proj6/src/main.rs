mod assembler;

use std::{env::args, process::exit, fs::read_to_string, fs::write};

use assembler::Assembler;

const ERR_MSG: &'static str = "usage: assembler prog.asm";

fn main() 
{
    // Resolve arguments
    let args: Vec<String> = args().collect();
    let asm_file_path = match args.get(1)
    {
        Some(fname) => if args.len() == 2 { fname } else { eprintln!("{}", ERR_MSG); exit(1); }
        None => { eprintln!("{}", ERR_MSG); exit(1); }
    };

    // Read in assembly file
    let asm_file_contents: String = match read_to_string(asm_file_path)
    {
        Ok(contents) => contents,
        Err(_) => {
            eprintln!("{}\n{}", ERR_MSG, format!("unable to read file {}", asm_file_path));
            exit(1);
        }
    };

    // Translate/assemble code
    let mut assembler: Assembler = Assembler::new(&asm_file_contents);
    let translated_code_bin: Vec<String> = assembler.translate();

    // Output file
    let split_in_path: Vec<&str> = asm_file_path.split(".").collect::<Vec<&str>>();
    let out_path = split_in_path[..split_in_path.len() - 1].to_vec().join("") + ".hack";

    write(out_path, translated_code_bin.join("\n")).unwrap();
}