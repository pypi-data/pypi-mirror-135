module decouple #(
		              // {{{
		              parameter	[0:0]	OPT_LOWPOWER = 0,
		              parameter	[0:0]	OPT_OUTREG = 1,
		              //
		              parameter	[0:0]	OPT_PASSTHROUGH = 0,
		              parameter	[0:0]	OPT_INITIAL = 1'b1
		              // }}}
                  ) (
                     input logic clk,
                     input logic rst,
                     dti.consumer din,
                     dti.producer dout
	                   );

   logic [$size(din.data)-1:0]   r_data;
   logic                         r_valid;

   initial r_valid = 0;
   always @(posedge clk)
     if (rst)
       r_valid <= 0;
     else if ((din.valid && din.ready) && (dout.valid && !dout.ready))
       r_valid <= 1;
     else if (dout.ready)
       r_valid <= 0;

   always @(posedge clk)
     if (din.valid && din.ready)
       r_data <= din.data;

   always @(*)
     din.ready = !r_valid;

   initial dout.valid = 0;
   always @(posedge clk)
     if (rst)
       dout.valid <= 0;
     else if (!dout.valid || dout.ready)
       dout.valid <= (din.valid || r_valid);

   always @(posedge clk)
     if (!dout.valid || dout.ready) begin
        if (r_valid)
          dout.data <= r_data;
        else
          dout.data <= din.data;
     end

endmodule
