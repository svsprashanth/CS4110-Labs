@0
D=M
@1
D=D-M
@GT
D; JGT

@LT
D; JLT

@E
D; JEQ

(GT)
@2
D=1
M=D
@END
0,JMP

(LT)
@2
D=1
D=D+1
M=D
@END
0,JMP

(E)
@2
D=0
M=D
@END
0,JMP

(END)
@END
0;JMP