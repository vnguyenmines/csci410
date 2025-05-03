// Bootstrap code, initialize SP to 256 and call Sys.init:
@256
D=A
@SP
M=D
@Sys.init$ret.0
D=A
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Reposition ARG:
@5
D=A
@SP
D=M-D
@ARG
M=D
// Reposition LCL:
@SP
D=M
@LCL
M=D
// Select label `Sys.init:
@Sys.init
// Go to label `Sys.init` (unconditional goto):
0;JMP
// Create label `Sys.init$ret.0:
(Sys.init$ret.0)
// Prepare to push from local, argument, this or that segment into D:
@ARG
D=M
@1
A=D+A
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Store address of pointer 1 in register 13:
// Store address for pointer (THIS/THAT):
@THAT
D=A
@13
M=D
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Push a constant into D:
@0
D=A
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Store address of that 0 in register 13:
@THAT
D=M
@0
D=D+A
@13
M=D
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Push a constant into D:
@1
D=A
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Store address of that 1 in register 13:
@THAT
D=M
@1
D=D+A
@13
M=D
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Prepare to push from local, argument, this or that segment into D:
@ARG
D=M
@0
A=D+A
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Push a constant into D:
@2
D=A
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
// Pop the other operand and perform a binary operation; save result in D:
@SP
M=M-1
A=M
D=M-D
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Store address of argument 0 in register 13:
@ARG
D=M
@0
D=D+A
@13
M=D
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Create label `LOOP:
(LOOP)
// Prepare to push from local, argument, this or that segment into D:
@ARG
D=M
@0
A=D+A
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
// If the value in D is not false, go to `COMPUTE_ELEMENT` (if-goto):
// Select label `COMPUTE_ELEMENT:
@COMPUTE_ELEMENT
D;JNE
// Select label `END:
@END
// Go to label `END` (unconditional goto):
0;JMP
// Create label `COMPUTE_ELEMENT:
(COMPUTE_ELEMENT)
// Prepare to push from local, argument, this or that segment into D:
@THAT
D=M
@0
A=D+A
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Prepare to push from local, argument, this or that segment into D:
@THAT
D=M
@1
A=D+A
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
// Pop the other operand and perform a binary operation; save result in D:
@SP
M=M-1
A=M
D=D+M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Store address of that 2 in register 13:
@THAT
D=M
@2
D=D+A
@13
M=D
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Push from pointer segment (THIS/THAT) into D:
@THAT
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Push a constant into D:
@1
D=A
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
// Pop the other operand and perform a binary operation; save result in D:
@SP
M=M-1
A=M
D=D+M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Store address of pointer 1 in register 13:
// Store address for pointer (THIS/THAT):
@THAT
D=A
@13
M=D
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Prepare to push from local, argument, this or that segment into D:
@ARG
D=M
@0
A=D+A
D=M
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Push a constant into D:
@1
D=A
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
// Pop the other operand and perform a binary operation; save result in D:
@SP
M=M-1
A=M
D=M-D
// Push the value in the register D onto the stack:
@SP
A=M
M=D
@SP
M=M+1
// Store address of argument 0 in register 13:
@ARG
D=M
@0
D=D+A
@13
M=D
// Pop the top value from the stack into register D:
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// Select label `LOOP:
@LOOP
// Go to label `LOOP` (unconditional goto):
0;JMP
// Create label `END:
(END)
// End the program with an infinite loop:
(END_PROGRAM)
@END_PROGRAM
0;JMP
