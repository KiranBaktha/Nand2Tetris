// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(START)
   @base  // base is the counter variable which will start from the first register of the screen and end at the last
   M =-1
(MAIN)
   @base
   M = M+1
   D = M
   @8192  // Check if max count has been reached
   D = A-D
   @HALT0
   D;JEQ
   @base
   D=M
   @SCREEN
   A=A+D // Go to the next register in order
   M=0  // All bits in the register set to 0
   @24576  // Check input
   D = M
   @STARTACTIVATION // Start to blacken the screen
   D;JNE
   @MAIN
   0;JMP
(STARTACTIVATION)
   @base // Initialize base counter again
   M =-1 
(ACTIVATION)
   @base
   M = M+1
   D = M
   @8192
   D = A-D
   @HALT1
   D;JEQ
   @base
   D=M
   @SCREEN
   A=A+D  // Go to the next register in order
   M=-1 // All bits in the register set to 1
   @24576 // Check input
   D = M
   @ACTIVATION
   D;JNE
   @START // Input has changed to 0 from keyboard so go back to start 
   0;JMP
(HALT1) // The screen is fully blackened wait here until keyboard input is 0
   @24576
   D=M
   @START
   D;JEQ
   @HALT1
   0;JMP
(HALT0) // The screen is fully whitened wait here until keyboard input is not 0
   @24576
   D=M
   @STARTACTIVATION
   D;JNE
   @HALT0
   0;JMP