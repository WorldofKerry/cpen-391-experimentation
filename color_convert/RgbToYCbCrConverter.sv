module Rgb_To_YCbCr (
    input clk,
    input rst,
    input [7:0] r,
    input [7:0] g,
    input [7:0] b,
    output reg [7:0] y,
    output reg [7:0] cb,
    output reg [7:0] cr
);

    always @(posedge clk) begin
        if (rst) begin
            y <= 8'h00;
            cb <= 8'h00;
            cr <= 8'h00;
        end else begin
            y <= 16+(((r<<6)+(r<<1)+(g<<7)+g+(b<<4)+(b<<3)+b)>>8);
            cb <= 128 + ((-((r<<5)+(r<<2)+(r<<1))-((g<<6)+(g<<3)+(g<<1))+(b<<7)-(b<<4))>>8);
            cr <= 128 + (((r<<7)-(r<<4)-((g<<6)+(g<<5)-(g<<1))-((b<<4)+(b<<1)))>>8);
        end
    end

endmodule