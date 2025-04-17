use std::{fs::{File, OpenOptions}, io::Write};

pub struct CodeWriter
{
    _file: File
}

impl CodeWriter
{
    pub fn new(out_file_path: &String) -> Self
    {
        Self {
            _file: OpenOptions::new().append(true).write(true).create(true).open(out_file_path).expect(format!("Unable to work with file {}", out_file_path).as_str()),
           }
    }

    /// Writes a comment out to the asm file for logging purposes
    pub fn write_comment(&self, msg: &String)
    {
        writeln!(&self._file, "// {}", msg).expect("Unable to write to output file");
    }

    /// Writes the assembly code out to the .asm output file
    pub fn write_code(&self, lines: Vec<String>)
    {
        lines.iter().for_each(|x| writeln!(&self._file, "{}", x).expect("Unable to write to output file"));
    }
}