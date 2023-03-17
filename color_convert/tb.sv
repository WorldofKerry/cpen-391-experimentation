// Testbench
module test;

  reg clk;
  reg reset;
  
  logic [7:0] r, g, b, y, cb, cr; 
  
  RgbToYCbCr dut (
      // module ports
    .clk(clk),
    .rst(reset),
    .r(r),
    .g(g),
    .b(b),
    .y(y),
    .cb(cb),
    .cr(cr)
    );
  
  logic [7:0] r_in [0:7] = '{64, 128, 192, 255, 0, 128, 0, 255};
  logic [7:0] g_in [0:7] = '{0, 64, 128, 192, 128, 0, 255, 128};
  logic [7:0] b_in [0:7] = '{128, 192, 255, 0, 128, 255, 128, 0};
  
  integer i; 
  
  always #5 clk = ~clk; 
          
  initial begin
    // Dump waves
    $dumpfile("dump.vcd");
    $dumpvars(1);
    clk = 0; 
    
    @(posedge clk); 
    reset = 1; 
    @(posedge clk); 
    reset = 0; 
    
    $display("Starting Loop.");
    for (i = 0; i < 8; i = i + 1) begin
      r = r_in[i];
      g = g_in[i];
      b = b_in[i]; 
      @(posedge clk); 
      @(posedge clk); 
      $display("%d,%d,%d %d,%d,%d", r, g, b, y, cb, cr); 
    end
    
    $finish; 
  end 
endmodule