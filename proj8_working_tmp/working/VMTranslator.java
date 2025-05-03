import java.io.File;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.io.BufferedReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class VMTranslator {
    public static void main(String[] args) {
        try {
            // Check if the input path was provided as a command-line argument
            if (args.length == 0) {
                System.out.println("Error: No input path provided.");
                return;
            }
            
            // Extract the file or directory path
            String inputPath = args[0];
            File inputFile = new File(inputPath);
            
            // Check if input exists
            if (!inputFile.exists()) {
                System.out.println("Error: Input path does not exist.");
                return;
            }
            
            // Determine output file path
            String outputPath;
            List<File> vmFiles = new ArrayList<>();
            

            if (inputFile.isDirectory()) {
                // If input is a directory, get all .vm files
                outputPath = inputPath + File.separator + inputFile.getName() + ".asm";
                vmFiles = Arrays.stream(inputFile.listFiles())
                    .filter(file -> file.getName().endsWith(".vm"))
                    .collect(Collectors.toList());
                
                if (vmFiles.isEmpty()) {
                    System.out.println("Error: No .vm files found in the directory.");
                    return;
                }
            } else {
                // If input is a single file
                if (!inputPath.endsWith(".vm")) {
                    System.out.println("Error: Input file must have .vm extension.");
                    return;
                }
                
                outputPath = inputPath.substring(0, inputPath.length() - 3) + ".asm";
                vmFiles.add(inputFile);
            }
            
            // Create FileWriter for the output .asm file
            try (FileWriter assemblyFile = new FileWriter(outputPath)) {
                int labelCounter = 0; 
                if (vmFiles.size() > 1) {
                    // Set stack pointer to 256
                    assemblyFile.write("""
                        // Bootstrap code
                        @256
                        D=A
                        @SP
                        M=D
                        """);
                    
                    // Call Sys.init
                    CodeWriter bootstrapCodeWriter = new CodeWriter("Bootstrap");
                    String sysInitCall = bootstrapCodeWriter.callCommand("Sys.init", 0, labelCounter++);
                    assemblyFile.write(sysInitCall);
                }
        
                // Process each .vm file
                for (File vmFile : vmFiles) {
                    String vmFileName = vmFile.getName().substring(0, vmFile.getName().length() - 3);
                    
                    CodeWriter codeWriter = new CodeWriter(vmFileName);

                    try (BufferedReader reader = new BufferedReader(new FileReader(vmFile))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            // Trim and ignore comments and empty lines
                            line = line.trim();
                            if (line.isEmpty() || line.startsWith("//")) {
                                continue;
                            }
                            
                            // Remove inline comments
                            int commentIndex = line.indexOf("//");
                            if (commentIndex != -1) {
                                line = line.substring(0, commentIndex).trim();
                            }
                            
                            // Translate VM command to Assembly
                            String[] parts = line.split("\\s+");
                            String asmCode = "";
                            
                            try {
                                if (parts.length == 1) {
                                    // Arithmetic/Logical commands And return 
                                    if (parts[0].equals("add")) {
                                        asmCode = codeWriter.addCommand();
                                    } else if (parts[0].equals("sub")) {
                                        asmCode = codeWriter.subCommand();
                                    } else if (parts[0].equals("neg")) {
                                        asmCode = codeWriter.negCommand();
                                    } else if (parts[0].equals("eq")) {
                                        asmCode = codeWriter.eqCommand(labelCounter++);
                                    } else if (parts[0].equals("gt")) {
                                        asmCode = codeWriter.gtCommand(labelCounter++);
                                    } else if (parts[0].equals("lt")) {
                                        asmCode = codeWriter.ltCommand(labelCounter++);
                                    } else if (parts[0].equals("and")) {
                                        asmCode = codeWriter.andCommand();
                                    } else if (parts[0].equals("or")) {
                                        asmCode = codeWriter.orCommand();
                                    } else if (parts[0].equals("not")) {
                                        asmCode = codeWriter.notCommand();
                                    } else if (parts[0].equals("return")) {
                                        asmCode = codeWriter.returnCommand();
                                    } else {
                                        System.out.println("Unknown command: " + line);
                                        asmCode = "";
                                    }
                                } else if (parts.length == 2) {
                                    // Label and if and goto
                                    if (parts[0].equals("label")) {
                                        asmCode = codeWriter.labelCode(parts[1]);
                                    } else if (parts[0].equals("goto")) {
                                        asmCode = codeWriter.gotoCode(parts[1]);
                                    } else if (parts[0].equals("if-goto")) {
                                        asmCode = codeWriter.ifCode(parts[1]);
                                    } else {
                                        System.out.println("Unknown command: " + line);
                                        asmCode = "";
                                    }
                                } else if (parts.length == 3) {
                                    try {
                                        // push, pop, and function calls
                                        int arg = Integer.parseInt(parts[2]);
                                        if (parts[0].equals("push")) {
                                            asmCode = codeWriter.pushCode(parts[1], arg);
                                        } else if (parts[0].equals("pop")) {
                                            asmCode = codeWriter.popCode(parts[1], arg, labelCounter++);
                                        } else if (parts[0].equals("function")) {
                                            asmCode = codeWriter.functionCommand(parts[1], arg);
                                        } else if (parts[0].equals("call")) {
                                            asmCode = codeWriter.callCommand(parts[1], arg, labelCounter++);
                                        } else {
                                            System.out.println("Unknown command: " + line);
                                            asmCode = "";
                                        }
                                    } catch (NumberFormatException e) {
                                        System.out.println("Error parsing number in line: " + line);
                                        e.printStackTrace();
                                    }
                                } else {
                                    System.out.println("Invalid command: " + line);
                                }
                                
                            } catch (Exception e) {
                                System.out.println("Error processing line: " + line);
                                e.printStackTrace();
                            }
                            
                            assemblyFile.write(asmCode);
                        }
                    }
                }
                
                System.out.println("Translation complete. Output written to " + outputPath);
            }
        } catch (IOException e) {
            System.out.println("An error occurred during translation: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    static class CodeWriter {
        private String filename;

        // private int labelCounter = 0;
        
        public CodeWriter(String filename) {
            this.filename = filename;
        }

        public String callCommand(String functionName, int numArgs, int labelNum) {
            return String.format("""
                // call %s %d
                // Push return address
                @return.%s.%d
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                
                // Push LCL
                @LCL
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                
                // Push ARG
                @ARG
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                
                // Push THIS
                @THIS
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                
                // Push THAT
                @THAT
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                
                // Reposition ARG: SP-5-nArgs
                @SP
                D=M
                @%d
                D=D-A
                @5
                D=D-A
                @ARG
                M=D
                
                // Set LCL to current SP
                @SP
                D=M
                @LCL
                M=D
                
                // Jump to function
                @%s
                0;JMP
                
                // Return label
                (return.%s.%d)
                """, functionName, numArgs, functionName, labelNum, numArgs, functionName, functionName, labelNum);
        }
        
        public String functionCommand(String functionName, int numLocals) {
            StringBuilder functionCode = new StringBuilder();
            
            // Create function label
            functionCode.append(String.format("// function %s %d\n", functionName, numLocals));
            functionCode.append(String.format("(%s)\n", functionName));
            
            // Initialize local variables to 0
            for (int i = 0; i < numLocals; i++) {
                functionCode.append("""
                    @SP
                    A=M
                    M=0
                    @SP
                    M=M+1
                    """);
            }
            
            return functionCode.toString();
        }
        
        public String returnCommand() {
            return """
                // return
                // FRAME = LCL
                @LCL
                D=M
                @R13   // FRAME stored in R13
                M=D
                
                // RET = *(FRAME-5)
                @5
                A=D-A
                D=M
                @R14   // Return address in R14
                M=D
                
                // *ARG = pop()
                @SP
                AM=M-1
                D=M
                @ARG
                A=M
                M=D
                
                // SP = ARG+1
                @ARG
                D=M+1
                @SP
                M=D
                
                // THAT = *(FRAME-1)
                @R13
                AM=M-1
                D=M
                @THAT
                M=D
                
                // THIS = *(FRAME-2)
                @R13
                AM=M-1
                D=M
                @THIS
                M=D
                
                // ARG = *(FRAME-3)
                @R13
                AM=M-1
                D=M
                @ARG
                M=D
                
                // LCL = *(FRAME-4)
                @R13
                AM=M-1
                D=M
                @LCL
                M=D
                
                // goto RET
                @R14
                A=M
                0;JMP
            """;
        }

        public String eqCommand(int localLabelCounter) {
            String labelTrue = "EQ_TRUE" + localLabelCounter;
            String labelEnd = "EQ_END" + localLabelCounter;
            return String.format("""
                // EQ command
                @SP
                A=M-1
                D=M
                @SP
                A=M-2
                D=D-M
                @%s
                D;JEQ
                @%s
                0;JMP
                (%s)
                """, labelTrue, labelEnd, labelTrue);
        }
        
        public String addCommand() {
            return """
                   // add
                   @SP
                   M=M-1
                   A=M
                   D=M
                   A=A-1
                   M=D+M
                   
                   """;
        }
    
        public String subCommand() {
            return """
                   // sub
                   @SP
                   M=M-1
                   A=M
                   D=M
                   A=A-1
                   M=M-D
                   
                   """;
        }
    
        public String negCommand() {
            return """
                   // neg
                   @SP
                   A=M-1
                   M=-M
                   
                   """;
        }
    
        public String gtCommand(int label) {
            return String.format("""
                   // gt
                   @SP
                   M=M-1
                   A=M
                   D=M
                   A=A-1
                   D=M-D
                   @GT_%d
                   D;JGT
                   @SP
                   A=M-1
                   M=0
                   @END_%d
                   0;JMP
                   (GT_%d)
                   @SP
                   A=M-1
                   M=-1
                   (END_%d)
                   
                   """, label, label, label, label);
        }
    
        public String ltCommand(int label) {
            return String.format("""
                   // lt
                   @SP
                   M=M-1
                   A=M
                   D=M
                   A=A-1
                   D=M-D
                   @LT_%d
                   D;JLT
                   @SP
                   A=M-1
                   M=0
                   @END_%d
                   0;JMP
                   (LT_%d)
                   @SP
                   A=M-1
                   M=-1
                   (END_%d)
                   
                   """, label, label, label, label);
        }
    
        public String andCommand() {
            return """
                   // and
                   @SP
                   M=M-1
                   A=M
                   D=M
                   A=A-1
                   M=D&M
                   
                   """;
        }
    
        public String orCommand() {
            return """
                   // or
                   @SP
                   M=M-1
                   A=M
                   D=M
                   A=A-1
                   M=D|M
                   
                   """;
        }
    
        public String notCommand() {
            return """
                   // not
                   @SP
                   A=M-1
                   M=!M
                   
                   """;
        }
    
        public String pushCode(String segment, int index) {
            switch (segment) {
                case "static":
                // Use fully qualified static variable name
                return String.format("""
                    // push static %d
                    @%s.%d
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    
                    """, index, filename, index);

                case "constant":
                    return String.format("""
                        // push constant %d
                        @%d
                        D=A
                        @SP
                        A=M
                        M=D
                        @SP
                        M=M+1
                        
                        """, index, index);
                case "local":
                    return String.format("""
                           // push local %d
                           @LCL
                           D=M
                           @%d
                           A=D+A
                           D=M
                           @SP
                           A=M
                           M=D
                           @SP
                           M=M+1
                           
                           """, index, index);
                case "argument":
                    return String.format("""
                           // push argument %d
                           @ARG
                           D=M
                           @%d
                           A=D+A
                           D=M
                           @SP
                           A=M
                           M=D
                           @SP
                           M=M+1
                           
                           """, index, index);
                case "this":
                    return String.format("""
                           // push this %d
                           @THIS
                           D=M
                           @%d
                           A=D+A
                           D=M
                           @SP
                           A=M
                           M=D
                           @SP
                           M=M+1
                           
                           """, index, index);
                case "that":
                    return String.format("""
                           // push that %d
                           @THAT
                           D=M
                           @%d
                           A=D+A
                           D=M
                           @SP
                           A=M
                           M=D
                           @SP
                           M=M+1
                           
                           """, index, index);
                case "pointer":
                    return String.format("""
                        // push pointer %d
                        @%s
                        D=M
                        @SP
                        A=M
                        M=D
                        @SP
                        M=M+1
                        """, index, (index == 0 ? "THIS" : "THAT"));
                case "temp":
                    return String.format("""
                           // push temp %d
                           @%d
                           D=M
                           @SP
                           A=M
                           M=D
                           @SP
                           M=M+1
                           
                           """, index, 5 + index);
                default:
                    System.out.println("Unknown segment: " + segment);
                    return "";
            }
        }
        
        public String popCode(String segment, int index, int labelNum) {
            switch (segment) {
                case "static":
                return String.format("""
                    // pop static %d
                    @SP
                    AM=M-1
                    D=M
                    @%s.%d
                    M=D
                    
                    """, index, filename, index);
         

                case "local":
                    return String.format("""
                            // pop local %d
                            @LCL
                            D=M
                            @%d
                            D=D+A
                            @R13
                            M=D
                            @SP
                            AM=M-1
                            D=M
                            @R13
                            A=M
                            M=D
                            
                            """, index, index);
                case "argument":
                    return String.format("""
                            // pop argument %d
                            @ARG
                            D=M
                            @%d
                            D=D+A
                            @R13
                            M=D
                            @SP
                            AM=M-1
                            D=M
                            @R13
                            A=M
                            M=D
                            
                            """, index, index);
                case "this":
                    return String.format("""
                            // pop this %d
                            @THIS
                            D=M
                            @%d
                            D=D+A
                            @R13
                            M=D
                            @SP
                            AM=M-1
                            D=M
                            @R13
                            A=M
                            M=D
                            
                            """, index, index);
                case "that":
                    return String.format("""
                            // pop that %d
                            @THAT
                            D=M
                            @%d
                            D=D+A
                            @R13
                            M=D
                            @SP
                            AM=M-1
                            D=M
                            @R13
                            A=M
                            M=D
                            
                            """, index, index);
                case "pointer":
                    return String.format("""
                        // pop pointer %d
                        @SP
                        AM=M-1
                        D=M
                        @%s
                        M=D
                        """, index, (index == 0 ? "THIS" : "THAT"));
                        
                case "temp":
                    return String.format("""
                            // pop temp %d
                            @SP
                            AM=M-1
                            D=M
                            @%d
                            M=D
                            
                            """, index, 5 + index);
                default:
                    System.out.println("Unknown segment: " + segment);
                    return "";
            }
        }
    
        public String labelCode(String label) {
            return String.format("""
                   // label %s
                   (%s)
                   
                   """, label, label);
        }
    
        public String gotoCode(String label) {
            return String.format("""
                   // goto %s
                   @%s
                   0;JMP
                   
                   """, label, label);
        }
    
        public String ifCode(String label) {
            return String.format("""
                   // if-goto %s
                   @SP
                   AM=M-1
                   D=M
                   @%s
                   D;JNE
                   
                   """, label, label);
        }
    }
}
