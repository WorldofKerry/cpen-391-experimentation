This program increments the value displayed on the red LEDs of the DE1-SoC by 1.
 For this
program to function, the FPGA must be programmed with the DE1_SoC_Computer.rbf p
rogramming
file, and the lightweight HPS2FPGA bridge must be enabled.

To compile the program use the following command:

  gcc access_dram.c -o access_dram

Execute using:

  ./access_dram
