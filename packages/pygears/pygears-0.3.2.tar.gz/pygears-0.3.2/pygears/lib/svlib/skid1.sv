module decouple (
                 input logic clk,
                 input logic rst,
                             dti.consumer din,
                             dti.producer dout
	                   );

   logic [$size(din.data)-1:0]   din_ready_r;
   logic                         dout_valid_r;
   logic                         din_data_r;
   logic                         dout_data_r;

   initial din_ready_r = 0;
   always @(posedge clk)
     if (rst)
       din_ready_r <= 0;
     else if (dout.ready || (!dout.valid))
       din_ready_r <= 1;
     else if (din.valid)
       din_ready_r <= 0;

   initial dout_valid_r = 0;
   always @(posedge clk)
     if (rst)
       dout_valid_r <= 0;
     else if (din.valid || (!din.ready))
       dout_valid_r <= 1;
     else if (dout.ready)
       dout_valid_r <= 0;

   always @(posedge clk)
     if (din.valid && din.ready)
       r_data <= din.data;

   always @(posedge clk)
     if (dout.ready || (!dout.valid))
       if (din.ready)
         dout_data_r <= din.data;
       else
         dout_data_r <= din_data_r;

   assign dout.valid = dout_valid_r;
   assign din.ready = din_ready_r;
   assign dout.data = dout_data_r;


endmodule
