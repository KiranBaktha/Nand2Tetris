// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
   @R1
   D=M
   @R2 // Initialize R2 Register with value 0 for safety.
   M=0
   @END  // If R1 operand is 0 then jump to end.
   D;JEQ
   @R0
   D=M
   @END
   D;JEQ // If R0 operand is 0 then jump to end.
(LOOP)  // Sum R0, R1 times
   @R0
   D=M
   @R2
   M=D+M
   @R1
   M=M-1
   D=M
   @LOOP
   D;JGT
(END)
   @END
   0;JMP
   
   
