// Boilerplate bootstrap for Sys.init. Call Sys.init, initalize stack point to 256
@256
D=A
@SP
M=D

// Calling Sys.init 0
@FUNC_Sys.init_0_0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(FUNC_Sys.init_0_0)
// function Main.fibonacci 0
// Defining function Main.fibonacci
(Main.fibonacci)

// push argument 0
@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D-M
@SP
M=M-1
M=M-1
@LT_1
D;JLT
@SP
A=M
M=0
@END_1
0;JMP

(LT_1)
@SP
A=M
M=-1

(END_1)
@SP
M=M+1

// if-goto N_LT_2
@SP
M=M-1
A=M
D=M
@N_LT_2
D;JNE

// goto N_GE_2
@N_GE_2
0;JMP

// label N_LT_2
(N_LT_2)

// push argument 0
@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// return
@LCL
D=M
@STACK_FRAME
M=D
@5
D=D-A
A=D
D=M
@RETURN
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@STACK_FRAME
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@STACK_FRAME
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@STACK_FRAME
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@STACK_FRAME
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@RETURN
A=M
0;JMP

// label N_GE_2
(N_GE_2)

// push argument 0
@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D

// call Main.fibonacci 1
@FUNC_Main.fibonacci_1_2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(FUNC_Main.fibonacci_1_2)

// push argument 0
@0
D=A
@ARG
A=M
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D

// call Main.fibonacci 1
@FUNC_Main.fibonacci_1_3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(FUNC_Main.fibonacci_1_3)

// add
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M

// return
@LCL
D=M
@STACK_FRAME
M=D
@5
D=D-A
A=D
D=M
@RETURN
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@STACK_FRAME
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@STACK_FRAME
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@STACK_FRAME
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@STACK_FRAME
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@RETURN
A=M
0;JMP

// function Sys.init 0
// Defining function Sys.init
(Sys.init)

// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Main.fibonacci 1
@FUNC_Main.fibonacci_1_4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(FUNC_Main.fibonacci_1_4)

// label END
(END)

// goto END
@END
0;JMP
