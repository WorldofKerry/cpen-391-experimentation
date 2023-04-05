module rgb_to_ycbcr (
    input [7:0] iR,
    input [7:0] iG,
    input [7:0] iB,
    output [7:0] oY,
    output [7:0] oCb,
    output [7:0] oCr
);

    reg signed [31:0] r, g, b, cmax, cmin, delta, h;

    always @(*) begin
        r = $signed(iR);
        g = $signed(iG);
        b = $signed(iB);
        cmax = (iR > iG) ? (iR > iB) ? iR : iB : (iG > iB) ? iG : iB;
        cmin = (iR < iG) ? (iR < iB) ? iR : iB : (iG < iB) ? iG : iB;    
        delta = cmax - cmin; 
        if (delta == 0) begin
            h = 0;
        end else if (cmax == iR) begin
            h = g - b; 
        end else if (cmax == iG) begin
            h = b - r; 
        end else begin
            h = r - g;
        end
    end

    assign oY = h < 0 ? h + 360 : h;
    assign oCb = cmax; 
    assign oCr = cmin; 

endmodule