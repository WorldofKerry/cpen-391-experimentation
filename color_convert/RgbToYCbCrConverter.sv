module rgb_to_ycbcr (
    input [7:0] r,
    input [7:0] g,
    input [7:0] b,
    output [7:0] y,
    output [7:0] cb,
    output [7:0] cr
);

    assign y = 16+(((r<<6)+(r<<1)+(g<<7)+g+(b<<4)+(b<<3)+b)>>8);
    assign cb = 128 + ((-((r<<5)+(r<<2)+(r<<1))-((g<<6)+(g<<3)+(g<<1))+(b<<7)-(b<<4))>>8);
    assign cr = 128 + (((r<<7)-(r<<4)-((g<<6)+(g<<5)-(g<<1))-((b<<4)+(b<<1)))>>8);

endmodule