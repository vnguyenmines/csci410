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
// function Class1.set 0
// Defining function Class1.set
(Class1.set)

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

// pop static 0
@SP
AM=M-1
D=M
@STATIC_0_Class1
M=D

// push argument 1
@1
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

// pop static 1
@SP
AM=M-1
D=M
@STATIC_1_Class1
M=D

// push constant 0
@0
D=A
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

// function Class1.get 0
// Defining function Class1.get
(Class1.get)

// push static 0
@STATIC_0_Class1
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@STATIC_1_Class1
D=M
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

// function Class2.set 0
// Defining function Class2.set
(Class2.set)

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

// pop static 0
@SP
AM=M-1
D=M
@STATIC_0_Class2
M=D

// push argument 1
@1
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

// pop static 1
@SP
AM=M-1
D=M
@STATIC_1_Class2
M=D

// push constant 0
@0
D=A
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

// function Class2.get 0
// Defining function Class2.get
(Class2.get)

// push static 0
@STATIC_0_Class2
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@STATIC_1_Class2
D=M
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

// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class1.set 2
@FUNC_Class1.set_2_1
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
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(FUNC_Class1.set_2_1)

// pop temp 0
@0
D=A
@R5
D=D+A
@R5
M=D
@SP
M=M-1
A=M
D=M
@R5
A=M
M=D
@0
D=A
@R5
A=M
D=A-D
@R5
M=D

// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class2.set 2
@FUNC_Class2.set_2_2
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
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(FUNC_Class2.set_2_2)

// pop temp 0
@0
D=A
@R5
D=D+A
@R5
M=D
@SP
M=M-1
A=M
D=M
@R5
A=M
M=D
@0
D=A
@R5
A=M
D=A-D
@R5
M=D

// call Class1.get 0
@FUNC_Class1.get_0_3
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
@Class1.get
0;JMP
(FUNC_Class1.get_0_3)

// call Class2.get 0
@FUNC_Class2.get_0_4
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
@Class2.get
0;JMP
(FUNC_Class2.get_0_4)

// label END
(END)

// goto END
@END
0;JMP
